import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API 설정
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    # 수집 설정
    MAX_VIDEOS_PER_KEYWORD = int(os.getenv('MAX_VIDEOS_PER_KEYWORD', 25))
    MAX_CHANNELS_TO_ANALYZE = int(os.getenv('MAX_CHANNELS_TO_ANALYZE', 10))
    MIN_QUALITY_SCORE = int(os.getenv('MIN_QUALITY_SCORE', 50))
    
    # 디렉토리 설정
    DATA_DIR = "data"
    RAW_DATA_DIR = f"{DATA_DIR}/raw"
    PROCESSED_DATA_DIR = f"{DATA_DIR}/processed"
    EXPORTS_DIR = f"{DATA_DIR}/exports"
    
    # 로깅 설정
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/collection.log')

settings = Settings()
