#!/usr/bin/env python3
"""
Oxford Reading Tree Level 1 YouTube 콘텐츠 수집 메인 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors.youtube_collector import YouTubeCollector
from src.collectors.content_analyzer import ContentAnalyzer
from src.storage.json_handler import JSONHandler
from src.storage.csv_handler import CSVHandler
from config.settings import settings
from config.keywords import SEARCH_KEYWORDS
import logging

def setup_logging():
    """로깅 설정"""
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def main():
    """메인 수집 프로세스"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Oxford Reading Tree Level 1 YouTube 콘텐츠 수집 시작")
    
    # 컬렉터 초기화
    collector = YouTubeCollector(settings.YOUTUBE_API_KEY)
    analyzer = ContentAnalyzer()
    
    # 데이터 저장 핸들러
    json_handler = JSONHandler(settings.RAW_DATA_DIR)
    csv_handler = CSVHandler(settings.PROCESSED_DATA_DIR)
    
    # 수집 실행
    try:
        all_videos = []
        
        for keyword in SEARCH_KEYWORDS:
            logger.info(f"검색 키워드: {keyword}")
            videos = collector.search_videos(keyword, settings.MAX_VIDEOS_PER_KEYWORD)
            
            for video_data in videos:
                # 품질 분석
                quality_score = analyzer.calculate_quality_score(video_data)
                
                if quality_score >= settings.MIN_QUALITY_SCORE:
                    video_data.quality_score = quality_score
                    all_videos.append(video_data)
            
            time.sleep(1)  # API 제한 고려
        
        # 중복 제거 및 정렬
        unique_videos = remove_duplicates(all_videos)
        sorted_videos = sorted(unique_videos, key=lambda x: x.quality_score, reverse=True)
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_handler.save(sorted_videos, f"ort_level1_videos_{timestamp}.json")
        csv_handler.save(sorted_videos, f"ort_level1_videos_{timestamp}.csv")
        
        logger.info(f"수집 완료: {len(sorted_videos)}개 영상")
        
    except Exception as e:
        logger.error(f"수집 중 오류 발생: {e}")
        raise

if __name__ == "__main__":
    main()
