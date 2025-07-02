# english_study_planning_kids
phonix study and collecting contents from youtube

## 🚀 프로젝트 시작하기

### **1. 프로젝트 초기화**
```bash
# 프로젝트 디렉토리 생성
mkdir oxford-reading-tree-collector
cd oxford-reading-tree-collector

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 초기 설정 실행
python scripts/setup_project.py
```

### **2. 환경 설정**
```bash
# 환경변수 파일 설정
cp .env.template .env
# .env 파일을 열어서 YouTube API 키 입력

# 패키지 설치
pip install -r requirements.txt
```

### **3. 수집 실행**
```bash
# 메인 수집 스크립트 실행
python scripts/collect_videos.py

# 결과 분석
python scripts/analyze_results.py

# MCP 서버용 데이터 내보내기
python scripts/export_for_mcp.py
```

---

## 📊 예상 출력 구조

### **수집된 데이터 파일들**
```
data/
├── raw/
│   └── ort_level1_videos_20241202_143022.json    # 원시 수집 데이터
├── processed/
│   ├── ort_level1_videos_20241202_143022.csv     # 처리된 CSV
│   └── quality_analysis_report.json              # 품질 분석 리포트
└── exports/
    └── mcp_content_data.json                     # MCP 서버용 데이터
``` 
