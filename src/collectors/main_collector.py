"""메인 수집 orchestrator"""

import logging
import time
from typing import List, Dict, Set
from datetime import datetime

from .youtube_collector import YouTubeCollector
from .content_analyzer import ContentAnalyzer
from ..models.video_model import VideoData
from ..models.channel_model import ChannelData
from config.keywords import SEARCH_KEYWORDS

class MainCollector:
    def __init__(self, api_key: str, min_quality_score: int = 50):
        self.youtube_collector = YouTubeCollector(api_key)
        self.content_analyzer = ContentAnalyzer()
        self.min_quality_score = min_quality_score
        self.logger = logging.getLogger(__name__)
        
        # 수집 통계
        self.stats = {
            'total_searched': 0,
            'total_analyzed': 0,
            'high_quality_videos': 0,
            'channels_discovered': 0
        }
    
    def collect_oxford_reading_tree_level1(self) -> Dict[str, any]:
        """Oxford Reading Tree Level 1 콘텐츠 전체 수집 프로세스"""
        
        self.logger.info("🎯 Oxford Reading Tree Level 1 콘텐츠 수집 시작")
        start_time = datetime.now()
        
        all_videos = []
        channel_stats = {}
        
        # 1단계: 키워드 기반 영상 검색
        self.logger.info("📋 1단계: 키워드 기반 영상 검색")
        
        for i, keyword in enumerate(SEARCH_KEYWORDS, 1):
            self.logger.info(f"  ({i}/{len(SEARCH_KEYWORDS)}) 검색: '{keyword}'")
            
            videos = self.youtube_collector.search_videos(keyword, max_results=25)
            self.stats['total_searched'] += len(videos)
            
            # 각 영상 품질 분석
            for video in videos:
                quality_score = self.content_analyzer.calculate_quality_score(video)
                video.quality_score = quality_score
                video.is_level1_content = self.content_analyzer.is_level1_content(video)
                video.learning_objectives = self.content_analyzer.extract_learning_objectives(video)
                
                self.stats['total_analyzed'] += 1
                
                # 고품질 영상만 수집
                if quality_score >= self.min_quality_score:
                    all_videos.append(video)
                    self.stats['high_quality_videos'] += 1
                    
                    # 채널 통계 업데이트
                    self._update_channel_stats(channel_stats, video)
            
            # API 제한 준수
            time.sleep(1)
        
        # 2단계: 고품질 채널에서 추가 수집
        self.logger.info("🏆 2단계: 고품질 채널에서 추가 수집")
        
        high_quality_channels = self._identify_high_quality_channels(channel_stats)
        
        for channel_id, channel_info in high_quality_channels.items():
            self.logger.info(f"  추가 수집: {channel_info['name']}")
            
            additional_videos = self.youtube_collector.get_channel_videos(channel_id, max_results=15)
            
            for video in additional_videos:
                quality_score = self.content_analyzer.calculate_quality_score(video)
                video.quality_score = quality_score
                video.is_level1_content = self.content_analyzer.is_level1_content(video)
                video.learning_objectives = self.content_analyzer.extract_learning_objectives(video)
                
                if quality_score >= self.min_quality_score:
                    all_videos.append(video)
                    self.stats['high_quality_videos'] += 1
            
            time.sleep(2)  # 채널별 대기
        
        # 3단계: 데이터 정제 및 정렬
        self.logger.info("🔧 3단계: 데이터 정제 및 정렬")
        
        # 중복 제거
        unique_videos = self._remove_duplicates(all_videos)
        
        # 품질 점수로 정렬
        sorted_videos = sorted(unique_videos, key=lambda x: x.quality_score, reverse=True)
        
        # 최종 통계
        end_time = datetime.now()
        duration = end_time - start_time
        
        self.logger.info(f"✅ 수집 완료!")
        self.logger.info(f"  - 소요 시간: {duration}")
        self.logger.info(f"  - 검색된 영상: {self.stats['total_searched']}개")
        self.logger.info(f"  - 분석된 영상: {self.stats['total_analyzed']}개") 
        self.logger.info(f"  - 고품질 영상: {len(sorted_videos)}개")
        self.logger.info(f"  - 발견된 채널: {len(channel_stats)}개")
        
        return {
            'videos': sorted_videos,
            'channel_stats': channel_stats,
            'collection_stats': self.stats,
            'collection_time': duration,
            'timestamp': end_time
        }
    
    def _update_channel_stats(self, channel_stats: Dict, video: VideoData):
        """채널 통계 업데이트"""
        channel_id = video.channel_id
        
        if channel_id not in channel_stats:
            channel_stats[channel_id] = {
                'name': video.channel_title,
                'video_count': 0,
                'total_quality_score': 0,
                'videos': [],
                'avg_quality_score': 0
            }
        
        stats = channel_stats[channel_id]
        stats['video_count'] += 1
        stats['total_quality_score'] += video.quality_score
        stats['avg_quality_score'] = stats['total_quality_score'] / stats['video_count']
        stats['videos'].append(video)
    
    def _identify_high_quality_channels(self, channel_stats: Dict) -> Dict:
        """고품질 채널 식별"""
        high_quality_channels = {}
        
        for channel_id, stats in channel_stats.items():
            # 고품질 채널 기준:
            # 1. 2개 이상의 고품질 영상
            # 2. 평균 품질 점수 70점 이상
            if (stats['video_count'] >= 2 and 
                stats['avg_quality_score'] >= 70):
                
                high_quality_channels[channel_id] = stats
        
        # 상위 5개 채널만 추가 수집
        sorted_channels = sorted(
            high_quality_channels.items(),
            key=lambda x: x[1]['avg_quality_score'],
            reverse=True
        )
        
        return dict(sorted_channels[:5])
    
    def _remove_duplicates(self, videos: List[VideoData]) -> List[VideoData]:
        """중복 영상 제거"""
        seen_ids = set()
        unique_videos = []
        
        for video in videos:
            if video.video_id not in seen_ids:
                seen_ids.add(video.video_id)
                unique_videos.append(video)
        
        removed_count = len(videos) - len(unique_videos)
        if removed_count > 0:
            self.logger.info(f"  중복 제거: {removed_count}개 영상")
        
        return unique_videos

