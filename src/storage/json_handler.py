"""JSON 파일 저장/로드 핸들러"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime
import logging

from ..models.video_model import VideoData

class JSONHandler:
    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(base_dir, exist_ok=True)
    
    def save_videos(self, videos: List[VideoData], filename: str = None) -> str:
        """영상 데이터를 JSON으로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ort_level1_videos_{timestamp}.json"
        
        filepath = os.path.join(self.base_dir, filename)
        
        # VideoData 객체를 딕셔너리로 변환
        videos_data = []
        for video in videos:
            video_dict = video.dict()
            # datetime 객체를 ISO 형식 문자열로 변환
            video_dict['published_at'] = video.published_at.isoformat()
            videos_data.append(video_dict)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(videos_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"JSON 저장 완료: {filepath} ({len(videos)}개 영상)")
            return filepath
            
        except Exception as e:
            self.logger.error(f"JSON 저장 실패: {e}")
            raise
    
    def save_report(self, report: Dict[str, Any], filename: str = None) -> str:
        """수집 리포트를 JSON으로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"collection_report_{timestamp}.json"
        
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            # datetime 객체들을 문자열로 변환
            report_copy = json.loads(json.dumps(report, default=str))
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_copy, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"리포트 저장 완료: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"리포트 저장 실패: {e}")
            raise
    
    def load_videos(self, filepath: str) -> List[VideoData]:
        """JSON에서 영상 데이터 로드"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                videos_data = json.load(f)
            
            videos = []
            for video_dict in videos_data:
                # ISO 형식 문자열을 datetime 객체로 변환
                if isinstance(video_dict['published_at'], str):
                    video_dict['published_at'] = datetime.fromisoformat(video_dict['published_at'])
                
                video = VideoData(**video_dict)
                videos.append(video)
            
            self.logger.info(f"JSON 로드 완료: {filepath} ({len(videos)}개 영상)")
            return videos
            
        except Exception as e:
            self.logger.error(f"JSON 로드 실패: {e}")
            raise
