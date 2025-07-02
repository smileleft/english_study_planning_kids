from typing import Dict, List, Tuple
import re
from ..models.video_model import VideoData
from ..models.channel_model import ChannelData
from config.keywords import (
    POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS,
    TRUSTED_CHANNEL_INDICATORS, MIN_VIDEO_DURATION, MAX_VIDEO_DURATION
)

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
    

    def _analyze_title(self, title: str) -> int:
        """제목 분석 (최대 30점)"""
        score = 0
        title_lower = title.lower()
        
        # Oxford Reading Tree 명시 (+15점)
        if 'oxford reading tree' in title_lower:
            score += 15
        elif 'oxford' in title_lower and 'reading' in title_lower:
            score += 10
        
        # Level 1 명시 (+10점)
        if 'level 1' in title_lower or 'stage 1' in title_lower:
            score += 10
        
        # 캐릭터 이름 (+5점)
        characters = ['biff', 'chip', 'kipper', 'floppy']
        if any(char in title_lower for char in characters):
            score += 5
        
        return score


    def _analyze_description(self, description: str) -> int:
        """설명 분석 (최대 15점)"""
        score = 0
        desc_lower = description.lower()
        
        # 교육적 키워드 존재 (+10점)
        educational_keywords = ['phonics', 'learn', 'reading', 'education', 'children']
        keyword_count = sum(1 for keyword in educational_keywords if keyword in desc_lower)
        score += min(keyword_count * 2, 10)
        
        # 적절한 설명 길이 (+5점)
        if 50 <= len(description) <= 500:
            score += 5
        
        return score
    
    def _analyze_channel_trustworthiness(self, channel_title: str) -> int:
        """채널 신뢰도 분석 (최대 25점)"""
        score = 0
        channel_lower = channel_title.lower()
        
        # 공식/신뢰할 수 있는 채널 (+25점)
        for indicator in TRUSTED_CHANNEL_INDICATORS:
            if indicator in channel_lower:
                score += 25
                break
        else:
            # 교육 관련 키워드 (+10점)
            education_indicators = ['education', 'learning', 'school', 'teacher', 'kids']
            if any(indicator in channel_lower for indicator in education_indicators):
                score += 10
        
        return score
    
    def _analyze_engagement(self, view_count: int, like_count: int) -> int:
        """참여도 분석 (최대 15점)"""
        score = 0
        
        # 적절한 조회수 범위 (+10점)
        if 1000 <= view_count <= 500000:
            score += 10
        elif 500 <= view_count < 1000:
            score += 5
        
        # 좋아요 비율 (+5점)
        if view_count > 0 and like_count > 0:
            like_ratio = like_count / view_count
            if like_ratio >= 0.02:  # 2% 이상
                score += 5
            elif like_ratio >= 0.01:  # 1% 이상
                score += 3
        
        return score
    
    def _analyze_duration(self, duration_seconds: Optional[int]) -> int:
        """영상 길이 분석 (최대 10점)"""
        if not duration_seconds:
            return 0
        
        # Level 1 콘텐츠에 적절한 길이 (2-15분)
        if MIN_VIDEO_DURATION <= duration_seconds <= MAX_VIDEO_DURATION:
            # 5-10분이 가장 이상적
            if 300 <= duration_seconds <= 600:
                return 10
            else:
                return 7
        else:
            return 0
    
    def _check_inappropriate_content(self, title: str, description: str) -> int:
        """부적절한 콘텐츠 체크 (감점)"""
        content = f"{title} {description}".lower()
        
        penalty = 0
        for negative_keyword in NEGATIVE_KEYWORDS:
            if negative_keyword in content:
                penalty += 20  # 부적절한 키워드당 20점 감점
        
        return penalty
    
    def _calculate_recency_bonus(self, published_at) -> int:
        """최근성 보너스 (최대 5점)"""
        from datetime import datetime, timezone
        
        now = datetime.now(timezone.utc)
        days_old = (now - published_at).days
        
        if days_old <= 30:  # 1개월 이내
            return 5
        elif days_old <= 365:  # 1년 이내
            return 3
        elif days_old <= 1095:  # 3년 이내
            return 1
        else:
            return 0
    
    def is_level1_content(self, video: VideoData) -> bool:
        """Level 1 콘텐츠인지 판단"""
        content = f"{video.title} {video.description}".lower()
        
        # Level 1 직접 언급
        if 'level 1' in content or 'stage 1' in content:
            return True
        
        # Level 1 특징적 키워드들
        level1_keywords = [
            'first words', 'wordless', 'getting ready to read',
            'i see', 'up you go', 'get on', 'six in a bed'
        ]
        
        if any(keyword in content for keyword in level1_keywords):
            return True
        
        # 너무 어려운 내용은 제외
        advanced_keywords = [
            'level 2', 'level 3', 'chapter', 'advanced', 'complex'
        ]
        
        if any(keyword in content for keyword in advanced_keywords):
            return False
        
        # Oxford Reading Tree + 기본 캐릭터 = 높은 확률로 Level 1
        has_ort = 'oxford' in content and 'reading' in content
        has_characters = any(char in content for char in ['biff', 'chip', 'kipper'])
        
        return has_ort and has_characters
    
    def extract_learning_objectives(self, video: VideoData) -> List[str]:
        """학습 목표 추출"""
        objectives = []
        content = f"{video.title} {video.description}".lower()
        
        objective_mapping = {
            'alphabet': ['alphabet', 'abc', 'letters'],
            'phonics': ['phonics', 'sounds', 'letter sounds'],
            'first_words': ['first words', 'simple words', 'basic words'],
            'reading_readiness': ['getting ready', 'pre-reading', 'reading readiness'],
            'story_comprehension': ['story', 'comprehension', 'understanding'],
            'vocabulary': ['vocabulary', 'word recognition', 'sight words']
        }
        
        for objective, keywords in objective_mapping.items():
            if any(keyword in content for keyword in keywords):
                objectives.append(objective)
        
        return objectives
    
    def analyze_channel_quality(self, channel: ChannelData, videos: List[VideoData]) -> Tuple[int, float]:
        """채널 전체 품질 분석"""
        if not videos:
            return 0, 0.0
        
        # 영상별 품질 점수 평균
        quality_scores = [v.quality_score for v in videos if v.quality_score is not None]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # 채널 신뢰도 점수
        trustworthiness = self._analyze_channel_trustworthiness(channel.channel_name)
        
        # 구독자 수 기반 추가 점수
        if channel.subscriber_count >= 100000:
            trustworthiness += 10
        elif channel.subscriber_count >= 10000:
            trustworthiness += 5
        
        return min(trustworthiness, 100), avg_quality

