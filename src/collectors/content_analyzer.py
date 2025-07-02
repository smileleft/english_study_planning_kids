from typing import Dict, List
import re
from ..models.video_model import VideoData

class ContentAnalyzer:
    def __init__(self):
        self.ort_keywords = [
            'oxford reading tree', 'biff', 'chip', 'kipper', 
            'floppy', 'level 1', 'phonics', 'first words'
        ]
        self.trusted_channels = []  # 신뢰할 수 있는 채널 목록
    
    def calculate_quality_score(self, video: VideoData) -> int:
        """영상의 교육적 품질 점수 계산"""
        score = 0
        
        # 제목 분석
        score += self._analyze_title(video.title)
        
        # 채널 신뢰도
        score += self._analyze_channel(video.channel_title)
        
        # 조회수/좋아요 분석
        score += self._analyze_engagement(video.view_count, video.like_count)
        
        # 영상 길이 분석
        score += self._analyze_duration(video.duration)
        
        return min(score, 100)
    
    def is_level1_content(self, video: VideoData) -> bool:
        """Level 1 콘텐츠인지 판단"""
        pass
    
    def extract_learning_objectives(self, video: VideoData) -> List[str]:
        """학습 목표 추출"""
        pass
