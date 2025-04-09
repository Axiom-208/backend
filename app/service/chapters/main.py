from app.service.chapters.chapters import Chapters
import uuid

chapter = Chapters()
chapter.process_video_in_background(url = "https://www.youtube.com/watch?v=Cq7eND5KSPk", job_id = str(uuid.uuid4()))
