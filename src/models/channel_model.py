from pydantic import BaseModel
from typing import Optional, List

class ChannelData(BaseModel):
    channel_id: str
    channel_name: str
    description: str
    subscriber_count: int
    video_count: int
    view_count: int
    created_at: str
    
    # 분석 결과
    is_educational: Optional[bool] = None
    trustworthiness_score: Optional[int] = None
    ort_video_count: Optional[int] = None
    average_quality_score: Optional[float] = None
