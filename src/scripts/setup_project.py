#!/usr/bin/env python3
"""
프로젝트 초기 설정 스크립트
"""

import os
import sys

def create_directories():
    """필요한 디렉토리 생성"""
    directories = [
        'data/raw',
        'data/processed', 
        'data/exports',
        'logs',
        'tests',
        'src/collectors',
        'src/models',
        'src/utils',
        'src/storage',
        'config',
        'scripts',
        'docs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 디렉토리 생성: {directory}")

def create_init_files():
    """__init__.py 파일 생성"""
    init_files = [
        'src/__init__.py',
        'src/collectors/__init__.py',
        'src/models/__init__.py',
        'src/utils/__init__.py',
        'src/storage/__init__.py',
        'config/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# This file makes Python treat the directory as a package\n')
            print(f"✓ __init__.py 생성: {init_file}")

def create_gitignore():
    """gitignore 파일 생성"""
    gitignore_content = """# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Data files
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# Logs
logs/*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✓ .gitignore 파일 생성")

def create_env_template():
    """환경변수 템플릿 생성"""
    env_template = """# YouTube Data API 키 (https://console.developers.google.com에서 발급)
YOUTUBE_API_KEY=your_youtube_api_key_here

# 수집 설정
MAX_VIDEOS_PER_KEYWORD=25
MAX_CHANNELS_TO_ANALYZE=10
MIN_QUALITY_SCORE=50

# 로깅 설정
LOG_LEVEL=INFO
LOG_FILE=logs/collection.log
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_template)
    print("✓ .env.template 파일 생성")
    print("  → .env.template을 .env로 복사하고 실제 API 키를 입력하세요!")

def main():
    print("🚀 Oxford Reading Tree YouTube 수집 프로젝트 설정 시작\n")
    
    create_directories()
    print()
    
    create_init_files() 
    print()
    
    create_gitignore()
    create_env_template()
    
    print("\n✅ 프로젝트 설정 완료!")
    print("\n다음 단계:")
    print("1. .env.template을 .env로 복사")
    print("2. .env 파일에 YouTube API 키 입력")
    print("3. pip install -r requirements.txt 실행")
    print("4. python scripts/collect_videos.py 실행")

if __name__ == "__main__":
    main()
