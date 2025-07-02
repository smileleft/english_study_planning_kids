"""CSV 파일 저장/로드 핸들러"""

import csv
import os
import pandas as pd
from typing import List
from datetime import datetime
import logging

from ..models.video_model import VideoData

class CSVHandler:
    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(base_dir, exist_ok=True)
    
    def save_videos(self, videos: List[VideoData], filename: str = None) -> str:
        """영상 데이터를 CSV로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ort_level1_videos_{timestamp}.csv"
        
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            fieldnames = [
                'video_id', 'title', 'channel_title', 'url', 'quality_score',
                'is_level1_content', 'learning_objectives', 'view_count',
                'like_count', 'duration_seconds', 'published_at', 'thumbnail_url'
            ]
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for video in videos:
                    row = {
                        'video_id': video.video_id,
                        'title': video.title,
                        'channel_title': video.channel_title,
                        'url': video.url,
                        'quality_score': video.quality_score,
                        'is_level1_content': video.is_level1_content,
                        'learning_objectives': ', '.join(video.learning_objectives) if video.learning_objectives else '',
                        'view_count': video.view_count,
                        'like_count': video.like_count,
                        'duration_seconds': video.duration_seconds,
                        'published_at': video.published_at.isoformat(),
                        'thumbnail_url': video.thumbnail_url
                    }
                    writer.writerow(row)
            
            self.logger.info(f"CSV 저장 완료: {filepath} ({len(videos)}개 영상)")
            return filepath
            
        except Exception as e:
            self.logger.error(f"CSV 저장 실패: {e}")
            raise
    
    def save_summary_csv(self, videos: List[VideoData], filename: str = None) -> str:
        """요약된 CSV 저장 (주요 정보만)"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ort_level1_summary_{timestamp}.csv"
        
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            # pandas를 사용한 깔끔한 요약 테이블
            data = []
            for video in videos:
                data.append({
                    'Title': video.title[:60] + '...' if len(video.title) > 60 else video.title,
                    'Channel': video.channel_title,
                    'Quality Score': video.quality_score,
                    'Level 1 Content': 'Yes' if video.is_level1_content else 'No',
                    'Duration (min)': round(video.duration_seconds / 60, 1) if video.duration_seconds else 0,
                    'Views': f"{video.view_count:,}",
                    'URL': video.url
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            self.logger.info(f"요약 CSV 저장 완료: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"요약 CSV 저장 실패: {e}")
            raise
