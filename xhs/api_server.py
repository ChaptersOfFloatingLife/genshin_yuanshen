import os
import uuid
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl, field_validator
import uvicorn
from dataclasses import dataclass

from xhs.publish import publish_xhs_content
from xhs.utils import download_video, parse_tags


# Publishing task data structure
@dataclass
class PublishTask:
    scripts_data: dict
    publish_time: str
    video_path: str
    task_id: str


# Global queue and worker
publish_queue = asyncio.Queue()
worker_task = None


# Pydantic models for request/response validation
class ContentData(BaseModel):
    title: str
    script: str


class PublishRequest(BaseModel):
    name: str
    tags: Union[List[str], str]
    content: ContentData
    content_extra: str = ""
    video_url: Optional[HttpUrl] = None
    publish_time: Optional[str] = None
    
    @field_validator('publish_time')
    @classmethod
    def validate_publish_time(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d %H:%M')
            return v
        except ValueError:
            raise ValueError('publish_time must be in format "YYYY-MM-DD HH:MM"')


class PublishResponse(BaseModel):
    success: bool
    message: str
    task_id: str
    video_downloaded: bool = False
    scheduled_time: Optional[str] = None
    queue_position: Optional[int] = None


async def publish_worker():
    """Background worker to process publishing tasks sequentially."""
    while True:
        try:
            # Get next task from queue
            task = await publish_queue.get()
            
            print(f"Processing publish task {task.task_id}")
            
            # Publish content using existing function
            success = publish_xhs_content(
                scripts_data=task.scripts_data,
                publish_time=task.publish_time,
                video_path=task.video_path
            )
            
            if success:
                print(f"✅ Task {task.task_id} published successfully")
            else:
                print(f"❌ Task {task.task_id} failed to publish")
            
            # Clean up video file
            try:
                if os.path.exists(task.video_path):
                    os.remove(task.video_path)
                    print(f"🗑️ Cleaned up {task.video_path}")
            except Exception as e:
                print(f"Warning: Failed to cleanup {task.video_path}: {e}")
            
            # Mark task as done
            publish_queue.task_done()
            
        except Exception as e:
            print(f"Worker error: {e}")
            import traceback
            traceback.print_exc()


# Initialize FastAPI app
app = FastAPI(
    title="XHS Publisher API",
    description="HTTP API for publishing content to Xiaohongshu (Little Red Book)",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Start the background worker when server starts."""
    global worker_task
    worker_task = asyncio.create_task(publish_worker())
    print("🚀 Publishing worker started")


@app.post("/publish", response_model=PublishResponse)
async def publish_content(request: PublishRequest):
    """Publish content to XHS with optional video download."""
    
    try:
        # Generate unique task ID and video path
        task_id = uuid.uuid4().hex[:8]
        video_path = f"output/video_{task_id}.mp4"
        video_downloaded = False
        
        # Download video if URL provided (concurrent downloads are OK)
        if request.video_url:
            print(f"[{task_id}] Downloading video from: {request.video_url}")
            success = await download_video(str(request.video_url), video_path)
            if not success:
                raise HTTPException(
                    status_code=400, 
                    detail="Failed to download video from provided URL"
                )
            video_downloaded = True
        else:
            # Copy default video if no URL provided
            import shutil
            if os.path.exists("output/video.mp4"):
                shutil.copy("output/video.mp4", video_path)
        
        # Parse tags (handles both string and list formats)
        parsed_tags = parse_tags(request.tags)
        
        # Set default publish time if not provided (5 minutes from now)
        publish_time = request.publish_time
        if not publish_time:
            default_time = datetime.now() + timedelta(minutes=5)
            publish_time = default_time.strftime('%Y-%m-%d %H:%M')
        
        # Prepare content data in the format expected by the publish function
        scripts_data = {
            "name": request.name,
            "tags": parsed_tags,
            "content": {
                "title": request.content.title,
                "script": request.content.script
            },
            "content_extra": request.content_extra
        }
        
        # Create publish task and add to queue
        task = PublishTask(
            scripts_data=scripts_data,
            publish_time=publish_time,
            video_path=video_path,
            task_id=task_id
        )
        
        # Add task to queue for sequential processing
        await publish_queue.put(task)
        queue_size = publish_queue.qsize()
        
        print(f"[{task_id}] Queued for publishing (queue size: {queue_size})")
        
        return PublishResponse(
            success=True,
            message=f"Content queued for publishing (Task ID: {task_id})",
            task_id=task_id,
            video_downloaded=video_downloaded,
            scheduled_time=publish_time,
            queue_position=queue_size
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in publish endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "queue_size": publish_queue.qsize(),
        "worker_status": "running" if worker_task and not worker_task.done() else "stopped"
    }


@app.get("/queue/status")
async def queue_status():
    """Get current queue status."""
    return {
        "queue_size": publish_queue.qsize(),
        "worker_status": "running" if worker_task and not worker_task.done() else "stopped"
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "XHS Publisher API",
        "version": "1.0.0",
        "queue_size": publish_queue.qsize(),
        "endpoints": {
            "POST /publish": "Publish content to XHS (returns immediately, queues task)",
            "GET /health": "Health check with queue status",
            "GET /queue/status": "Current queue status", 
            "GET /docs": "API documentation"
        }
    }


@app.post("/")
async def root_post():
    """Handle POST requests to root - return helpful error."""
    raise HTTPException(
        status_code=400,
        detail={
            "error": "POST requests should be sent to /publish, not /",
            "correct_endpoint": "POST /publish",
            "example": {
                "name": "测试",
                "tags": "#测试",
                "content": {"title": "测试", "script": "测试内容"},
                "video_url": "https://example.com/video.mp4"
            }
        }
    )


def main():
    """Run the API server."""
    print("Starting XHS Publisher API server...")
    print("API docs available at: http://localhost:8000/docs")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )


if __name__ == "__main__":
    main()