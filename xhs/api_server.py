import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, field_validator
import uvicorn

from xhs.publish import publish_xhs_content
from xhs.utils import download_video, parse_tags


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
    video_downloaded: bool = False
    scheduled_time: Optional[str] = None


# Initialize FastAPI app
app = FastAPI(
    title="XHS Publisher API",
    description="HTTP API for publishing content to Xiaohongshu (Little Red Book)",
    version="1.0.0"
)


@app.post("/publish", response_model=PublishResponse)
async def publish_content(request: PublishRequest):
    """Publish content to XHS with optional video download."""
    
    try:
        video_downloaded = False
        video_path = "output/video.mp4"
        
        # Download video if URL provided
        if request.video_url:
            print(f"Downloading video from: {request.video_url}")
            success = await download_video(str(request.video_url), video_path)
            if not success:
                raise HTTPException(
                    status_code=400, 
                    detail="Failed to download video from provided URL"
                )
            video_downloaded = True
        
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
        
        # Publish to XHS
        print(f"Publishing content for {request.name} at {publish_time}")
        success = publish_xhs_content(
            scripts_data=scripts_data,
            publish_time=publish_time,
            video_path=video_path
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to publish content to XHS"
            )
        
        return PublishResponse(
            success=True,
            message="Content published successfully",
            video_downloaded=video_downloaded,
            scheduled_time=publish_time
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
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "XHS Publisher API",
        "version": "1.0.0",
        "endpoints": {
            "POST /publish": "Publish content to XHS",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        }
    }


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