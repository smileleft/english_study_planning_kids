"""메인 수집 실행 스크립트"""

#!/usr/bin/env python3

import sys
import os
import logging
from datetime import datetime

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors.main_collector import MainCollector
from src.utils.data_processing import DataProcessor
from src.storage.json_handler import JSONHandler
from src.storage.csv_handler import CSVHandler
from config.settings import settings

def setup_logging():
    """로깅 설정"""
    # 로그 디렉토리 생성
    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
    
    # 로깅 설정
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    """메인 수집 프로세스"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # API 키 확인
        if not settings.YOUTUBE_API_KEY or settings.YOUTUBE_API_KEY == 'your_youtube_api_key_here':
            logger.error("YouTube API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
            return
        
        logger.info("🎯 Oxford Reading Tree Level 1 YouTube 콘텐츠 수집 시작")
        
        # 필요한 디렉토리 생성
        os.makedirs(settings.RAW_DATA_DIR, exist_ok=True)
        os.makedirs(settings.PROCESSED_DATA_DIR, exist_ok=True)
        os.makedirs(settings.EXPORTS_DIR, exist_ok=True)
        
        # 메인 컬렉터 초기화
        collector = MainCollector(
            api_key=settings.YOUTUBE_API_KEY,
            min_quality_score=settings.MIN_QUALITY_SCORE
        )
        
        # 수집 실행
        collection_result = collector.collect_oxford_reading_tree_level1()
        
        # 데이터 처리
        processor = DataProcessor()
        report = processor.generate_collection_report(collection_result)
        mcp_data = processor.prepare_for_mcp(collection_result['videos'])
        
        # 저장 핸들러 초기화
        json_handler = JSONHandler(settings.RAW_DATA_DIR)
        csv_handler = CSVHandler(settings.PROCESSED_DATA_DIR)
        
        # 타임스탬프
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 데이터 저장
        logger.info("💾 수집 결과 저장 중...")
        
        # 1. 원시 영상 데이터 (JSON)
        json_handler.save_videos(
            collection_result['videos'], 
            f"ort_level1_videos_{timestamp}.json"
        )
        
        # 2. 처리된 영상 데이터 (CSV)
        csv_handler.save_videos(
            collection_result['videos'],
            f"ort_level1_videos_{timestamp}.csv"
        )
        
        # 3. 요약 CSV
        csv_handler.save_summary_csv(
            collection_result['videos'],
            f"ort_level1_summary_{timestamp}.csv"
        )
        
        # 4. 수집 리포트
        json_handler.save_report(
            report,
            f"collection_report_{timestamp}.json"
        )
        
        # 5. MCP 서버용 데이터
        mcp_filepath = os.path.join(settings.EXPORTS_DIR, f"mcp_content_{timestamp}.json")
        with open(mcp_filepath, 'w', encoding='utf-8') as f:
            import json
            json.dump(mcp_data, f, ensure_ascii=False, indent=2)
        logger.info(f"MCP 데이터 저장 완료: {mcp_filepath}")
        
        # 최종 결과 출력
        logger.info("\n" + "="*60)
        logger.info("📊 수집 완료 요약")
        logger.info("="*60)
        logger.info(f"🎥 총 수집 영상: {len(collection_result['videos'])}개")
        logger.info(f"📺 발견 채널: {len(collection_result['channel_stats'])}개")
        logger.info(f"⭐ 평균 품질 점수: {report['summary']['avg_quality_score']:.1f}점")
        logger.info(f"✅ Level 1 콘텐츠: {report['summary']['level1_videos']}개")
        logger.info(f"⏱️ 수집 시간: {collection_result['collection_time']}")
        
        print(f"\n🏆 상위 5개 고품질 영상:")
        for i, video in enumerate(collection_result['videos'][:5], 1):
            print(f"{i}. {video.title[:50]}...")
            print(f"   채널: {video.channel_title} | 점수: {video.quality_score}점")
            print(f"   URL: {video.url}\n")
        
        logger.info("✅ 모든 작업이 성공적으로 완료되었습니다!")
        
    except Exception as e:
        logger.error(f"❌ 수집 중 오류 발생: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
