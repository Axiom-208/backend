from fastapi import APIRouter, Depends, HTTPException
from starlette.exceptions import HTTPException


from app.service.chapters.chapters import Chapters
from app.core.dependencies import get_current_user
from app.models.user import UserModel
from app.schema.user import UserDocument

import json
from fastapi import Request
from typing import Dict
import uuid
from threading import Thread
from fastapi.responses import JSONResponse
import threading
import ffmpeg



router = APIRouter()
chapters_handler = Chapters()

@router.post('/api/clips/create')
async def create_clips(url: str):
    """API endpoint to create clips from a YouTube URL"""
    try:
        current_user = await get_current_user()
        if not current_user:
            return JSONResponse(
                status_code=401,
                content={'success': False, 'error': 'User not authenticated'}
            )
       

        if not url:
            return JSONResponse(
                status_code=400,
                content={'success': False, 'error': 'Missing Youtube URL'}
            )
        if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
            return JSONResponse(
                status_code=400,
                content={'success': False, 'error': 'Invalid Youtube URL'}
            )

        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Start processing in a background thread
        thread = Thread(target=chapters_handler.process_video_in_background, args=(url, job_id))
        thread.daemon = True
        thread.start()

        current_user.update(
            current_user.id,
            {"$push": {"chapters": job_id}}
        )

        return JSONResponse(
            status_code=202,
            content={
                'success': True,
                'job_id': job_id,
                'message': 'Processing started'
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'success': False, 'error': str(e)}
        )

@router.get('/{job_id}')
async def get_clips_status(job_id: str):
    """API endpoint to check status of a job generating clips"""
    if job_id not in chapters_handler.jobs:
        return JSONResponse(
            status_code=404,
            content={'success': False, 'error': 'Job not found'}
        )
    
    job_data = chapters_handler.jobs[job_id]
    return JSONResponse(
        status_code=200,
        content={
            'success': True,
            'job_id': job_id,
            'status': job_data['status'],
            'created_at': job_data['created_at'],
            'clips': job_data.get('clips', [])
        }
    )

@router.get("/user/clips")
async def get_clips_by_user(current_user: UserDocument = Depends(get_current_user)):
    try:
        jobs = [chapters_handler.jobs[job_id] for job_id in current_user.chapters if job_id in chapters_handler.jobs]
        clips = []
        for job in jobs:
            if job['status'] == 'completed':
                clips.extend(job.get('clips', []))
        
        return JSONResponse(
            status_code=200,
            content={
                'success': True,
                'clips': clips
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))