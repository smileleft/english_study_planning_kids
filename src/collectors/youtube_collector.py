from googleapiclient.discovery import build
from typing import List, Dict, Optional
import time
import logging
from ..models.video_model import VideoData
from ..models.channel_model import ChannelData

class YouTubeCollector:
    def __init__(self, api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.logger = logging.getLogger(__name__)
    
    def search_videos(self, query: str, max_results: int = 25) -> List[Dict]:
        """키워드로 영상 검색"""
        pass
    
    def get_video_details(self, video_id: str) -> Optional[VideoData]:
        """영상 상세 정보 가져오기"""
        pass
    
    def get_channel_info(self, channel_id: str) -> Optional[ChannelData]:
        """채널 정보 가져오기"""
        pass
    
    def get_channel_videos(self, channel_id: str, max_results: int = 25) -> List[Dict]:
        """채널의 영상 목록 가져오기"""
        pass
