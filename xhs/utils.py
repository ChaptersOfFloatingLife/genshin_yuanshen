import os
import httpx
from typing import List, Union
import re


async def download_video(video_url: str, output_path: str = "output/video.mp4") -> bool:
    """Download video from URL to specified path."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(video_url, follow_redirects=True)
            response.raise_for_status()
            
            with open(output_path, "wb") as f:
                f.write(response.content)
                
        print(f"Video downloaded: {output_path}")
        return True
        
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def parse_tags(tags: Union[str, List[str]]) -> List[str]:
    """Parse tags from string "#tag1 #tag2" or list ["tag1", "tag2"] format."""
    if isinstance(tags, list):
        return [tag.lstrip('#') for tag in tags]
    
    if isinstance(tags, str):
        # Extract hashtags: #tag1 #tag2 -> ["tag1", "tag2"]
        matches = re.findall(r'#(\w+)', tags)
        if matches:
            return matches
        # Fallback: split by spaces
        return [tag.strip().lstrip('#') for tag in tags.split() if tag.strip()]
    
    return []