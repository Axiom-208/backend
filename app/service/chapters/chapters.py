from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import ffmpeg
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import uuid
from datetime import datetime
from threading import Thread
import firebase_admin
from firebase_admin import credentials, storage

class Chapters:

    def __init__(self):
        # Set up
        load_dotenv()
        self.api_key=os.getenv("API_KEY")
        cred_path=os.getenv("FIREBASE_CREDENTIALS_PATH")
        bucket_name=os.getenv("FIREBASE_STORAGE_BUCKET")

        firebase_init = False
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'storageBucket': bucket_name
            })
            self.bucket = storage.bucket()
            firebase_init = True
        except Exception as e:
            print(f"Firebase Initialisation error: {e}")
            firebase_init = False

        # In-memory tracking for different jobs'
        self.jobs = {}


    # Functions
    def downloadVideo(self, url):
        """Given a url to a youtube video, it locally downloads the video"""
        video_filename = 'output.mp4'
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': video_filename,  # Output filename saved as output.mp4
            'merge_output_format': 'mp4',  # Force merged output to be MP4
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print("Video Downloaded")
                return video_filename
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def getAudio(self, video_path):
        """Given a video filepath as it's input, it converts the video to audio"""
        audio_filename = 'audio.mp3'
        try:
            (
                ffmpeg.input(video_path)
                .output(audio_filename, format='mp3', acodec='libmp3lame', ab='128k', vn=None)
                .run(overwrite_output=True)
            )

            print("Successfully converted to audio.mp3")
            return audio_filename
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def format_time(self, seconds):
        """Converts time from ss(seconds) to m:ss (minutes:seconds)"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds}"


    def generateTranscripts(self, audio_file):
        """Given an audio file, it uses OpenAi's whisper model to generate transcripts and stores it in a .txt file locally."""
        transcript_filename = 'transcripts.txt'

        try:
            # Passing audio through whisper
            client = OpenAI(api_key=self.api_key)
            with open(audio_file, 'rb') as f:
                transcription = client.audio.transcriptions.create(
                    file=f,
                    model="whisper-1",
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            # Storing them locally in a file
            with open(transcript_filename, 'w') as file:
                for segment in transcription.segments:
                    start_time = segment.start
                    end_time = segment.end
                    text = segment.text
                    file.write(f"Start{self.format_time(start_time)}, End: {self.format_time(end_time)}, Text: {text}\n")

            print("Transcript file generated as {transcript_filename}")

            # Return raw transcript content for next function
            full_transcript = " ".join([segment.text for segment in transcription.segments])
            return transcript_filename, full_transcript
        except Exception as e:
            print(f"An occurred during transcription: {e}")
            return None, None


    def transcriptHighlights(self, transcript):
        """Given a transcript, a model from OpenAI will analyse it and return back the highlights in JSON"""
        json_filename = 'topic_segments.json'

        try:
            client = OpenAI(api_key=self.api_key)
            # Have GPT model parse through the transcripts
            prompt = f"""
            Analyse this video transcript and identify distinct topic segments that would work well as 
            standalone clips for platforms like TikTok. For each segment, provide:
            1. A descriptive title
            2. The start time
            3. The end time

            Format your response as JSON with the following structure:
            {{
                "topics": [
                    {{
                        "title": "Topic Title",
                        "start_time": "m:ss",
                        "end_time": "m:ss"
                    }}
                ]
            }}

            Transcript:
            {transcript}
            """

            # API call to analyse the transcripts
            topic_response = client.chat.completions.create(
                model="gpt-4-turbo",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are an expert at identifying coherent topic segments in educational videos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            # Convert JSON response into python dictionary so we can use dict notation to parse through the segments
            topic_segments = json.loads(topic_response.choices[0].message.content)

            with open('topic_segments.json', 'w') as f:
                json.dump(topic_segments, f, indent=2)

            print("\nTOpic segments saved to 'topic_segments.json'")
            return json_filename, topic_segments
        except Exception as e:
            print(f"An error occurred during highlight analyse: {e}")
            return None, None
        
    def time_to_seconds(self, time_str):
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return int(parts[0])


    def trimVideo(self, video, segments):
        """Given the video file to trim and the segments in JSON format, it returns clips matching to the segment lengths and saves it a "chapters" folder in the current directory"""
        output_dir = "chapters"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        created_clips = []
        try:
            for i, topic in enumerate(segments['topics']):
                start = self.time_to_seconds(topic['start_time'])
                end = self.time_to_seconds(topic['end_time'])

                clean_title = ''.join(c if c.isalnum() or c in [' ', '_'] else '_' for c in topic['title'])
                clean_title = clean_title.replace(' ', '_')

                output_filename = f"{output_dir}/clip_{i+1}_{clean_title}.mp4"
                
                try:
                    (
                        ffmpeg
                        .input(video, ss=start, to=end)
                        .output(output_filename, c='copy')
                        .run(capture_stdout=True, capture_stderr=True)
                    )
                    blob = self.bucket.blob(output_filename)
                    blob.upload_from_filename(output_filename)
                    blob.make_public()
                    public_url = blob.public_url
                    created_clips.append({
                        'title': topic['title'],
                        'url': public_url
                    })
                    os.remove(output_filename)
                except Exception as e:
                    print(f"Error creating clip {i+1}: {e}")

            os.rmdir(output_dir)
            print("All clips have been created")
            return created_clips
        except Exception as e:
            print(f"an Error occurred during video trimming: {e}")
            return None

    def process_video_in_background(self, url, job_id):
        """Process video in a background thread"""
        self.jobs[job_id] = {
            'status': 'processing',
            'created_at': datetime.now().isoformat(),
            'clips': []
        }

        try:
            clips = self.main(url)

            if clips:
                self.jobs[job_id]['status'] = 'completed'
                self.jobs[job_id]['clips'] = clips
            else:
                self.jobs[job_id]['status'] = 'failed'
                self.jobs[job_id]['error'] = 'Failed to generate video'

            print(f"Finished processing video: {url}")
        except Exception as e:
            self.jobs[job_id]['status'] = 'failed'
            self.jobs[job_id]['error'] =  str(e)
            print(f"Error in background processing {e}")
        finally:
            temp_files = ['output.mp4', 'audio.mp3', 'transcripts.txt', 'topic_segments.json']
            for file in temp_files:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except Exception as e:
                        print(f"Error removing {file}: {e}")
        return

    def main(self, url, job_dir=None):
        """Main function to coordinate entire workflow"""
        print("Starting video processing workflow")
        video_path = self.downloadVideo(url)
        if not video_path:
            return 
        audio_path = self.getAudio(video_path)
        if not audio_path:
            return 
        
        transcript_path, transcript_content = self.generateTranscripts(audio_path)
        if not transcript_path or not transcript_content:
            print("Failed to generate transcripts. Exiting")
            return
        
        segments_path, segment_data = self.transcriptHighlights(transcript_content)
        if not segments_path or not segment_data:
            print("Failed to analyse transcript highlighting . Exiting")
            return
        
        clips = self.trimVideo(video_path, segment_data)
        if not clips:
            print("Failed to generate video clips. Exiting")
            return
        
        print("Video Processing Complete")
        return clips

