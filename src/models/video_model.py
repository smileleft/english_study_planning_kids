from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
