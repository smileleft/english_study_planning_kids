"""데이터 처리 유틸리티"""

import logging
from typing import List, Dict, Any
from datetime import datetime
import json

from ..models.video_model import VideoData

class DataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_collection_report(self, collection_result: Dict) -> Dict[str, Any]:
        """수집 결과 리포트 생성"""
        videos = collection_result['videos']
        channel_stats = collection_result['channel_stats']
        
        report = {
            'summary': {
                'total_videos': len(videos),
                'avg_quality_score': sum(v.quality_score for v in videos) / len(videos) if videos else 0,
                'level1_videos': sum(1 for v in videos if v.is_level1_content),
                'total_channels': len(channel_stats),
                'collection_time': str(collection_result['collection_time']),
                'timestamp': collection_result['timestamp'].isoformat()
            },
            'quality_distribution': self._analyze_quality_distribution(videos),
            'channel_analysis': self._analyze_channels(channel_stats),
            'learning_objectives': self._analyze_learning_objectives(videos),
            'top_videos': [self._video_to_dict(v) for v in videos[:10]]
        }
        
        return report
    
    def _analyze_quality_distribution(self, videos: List[VideoData]) -> Dict[str, int]:
        """품질 점수 분포 분석"""
        distribution = {
            'excellent (90-100)': 0,
            'good (70-89)': 0,
            'fair (50-69)': 0,
            'poor (0-49)': 0
        }
        
        for video in videos:
            score = video.quality_score
            if score >= 90:
                distribution['excellent (90-100)'] += 1
            elif score >= 70:
                distribution['good (70-89)'] += 1
            elif score >= 50:
                distribution['fair (50-69)'] += 1
            else:
                distribution['poor (0-49)'] += 1
        
        return distribution
    
    def _analyze_channels(self, channel_stats: Dict) -> Dict[str, Any]:
        """채널 분석"""
        top_channels = sorted(
            channel_stats.items(),
            key=lambda x: x[1]['avg_quality_score'],
            reverse=True
        )[:5]
        
        return {
            'top_channels': [
                {
                    'name': stats['name'],
                    'video_count': stats['video_count'],
                    'avg_quality_score': round(stats['avg_quality_score'], 1)
                }
                for channel_id, stats in top_channels
            ],
            'total_channels': len(channel_stats)
        }
    
    def _analyze_learning_objectives(self, videos: List[VideoData]) -> Dict[str, int]:
        """학습 목표 분석"""
        objectives_count = {}
        
        for video in videos:
            if video.learning_objectives:
                for objective in video.learning_objectives:
                    objectives_count[objective] = objectives_count.get(objective, 0) + 1
        
        return dict(sorted(objectives_count.items(), key=lambda x: x[1], reverse=True))
    
    def _video_to_dict(self, video: VideoData) -> Dict[str, Any]:
        """VideoData를 딕셔너리로 변환"""
        return {
            'video_id': video.video_id,
            'title': video.title,
            'channel_title': video.channel_title,
            'url': video.url,
            'quality_score': video.quality_score,
            'is_level1_content': video.is_level1_content,
            'learning_objectives': video.learning_objectives,
            'view_count': video.view_count,
            'duration_seconds': video.duration_seconds,
            'published_at': video.published_at.isoformat()
        }
    
    def prepare_for_mcp(self, videos: List[VideoData]) -> List[Dict[str, Any]]:
        """MCP 서버용 데이터 형식으로 변환"""
        mcp_data = []
        
        for video in videos:
            mcp_item = {
                'content_id': video.video_id,
                'title': video.title,
                'url': video.url,
                'content_type': 'youtube_video',
                'educational_level': 'oxford_reading_tree_level_1',
                'target_age': '3-4',
                'learning_objectives': video.learning_objectives or [],
                'quality_score': video.quality_score,
                'duration_minutes': round(video.duration_seconds / 60, 1) if video.duration_seconds else 0,
                'channel': video.channel_title,
                'is_level1_verified': video.is_level1_content,
                'metadata': {
                    'view_count': video.view_count,
                    'like_count': video.like_count,
                    'published_date': video.published_at.isoformat(),
                    'thumbnail_url': video.thumbnail_url
                }
            }
            mcp_data.append(mcp_item)
        
        return mcp_data

