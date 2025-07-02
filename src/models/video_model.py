from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import re

class VideoData(BaseModel):
    video_id: str
    title: str
    description: str
    channel_id: str
    channel_title: str
    published_at: datetime
    duration: str
    view_count: int
    like_count: int
    comment_count: int
    url: str
    thumbnail_url: str
    
    # 분석 결과
    quality_score: Optional[int] = None
    is_level1_content: Optional[bool] = None
    learning_objectives: Optional[List[str]] = None
    educational_rating: Optional[str] = None  # 'excellent', 'good', 'fair', 'poor'

    def __init__(self, **data):
        super().__init__(**data)
        if not self.url:
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"

        if self.duration and not self.duration_seconds:
            self.duration_seconds = self._parse_duration(self.duration)

    def _parse_duration(self, duration: str) -> int:
        """ISO 8601 duration을 초로 변환 (PT4M13S -> 253)"""
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration)
        if not match:
            return 0

        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)

        return hours * 3600 + minutes * 60 + seconds

    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
