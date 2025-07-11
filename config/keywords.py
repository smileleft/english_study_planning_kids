"""검색 키워드 및 분석 기준 정의"""

SEARCH_KEYWORDS = [
    # by character
    "Biff Chip Kipper Level 1",
    "Oxford Reading Tree Level 1 stories",
    "Biff Chip Kipper first words",
    "Oxford Reading Tree wordless stories",
    
    # by title
    "Oxford Reading Tree I See",
    "Oxford Reading Tree Up You Go", 
    "Oxford Reading Tree Get On",
    "Oxford Reading Tree A Good Trick",
    "Oxford Reading Tree Six in a Bed",
    "Oxford Reading Tree The Pancake",
    "Floppy Did This Oxford Reading Tree",
    
    # by educational purpose
    "Oxford Reading Tree phonics Level 1",
    "Biff Chip Kipper reading aloud",
    "Oxford Reading Tree for beginners",
    "English reading for 3 year olds Oxford",
    
    # by channel and series
    "Read with Oxford Level 1",
    "Oxford Owl Level 1",
    "Biff Chip Kipper story time"
]

# 교육적 품질 평가 키워드
POSITIVE_KEYWORDS = [
    'oxford reading tree', 'phonics', 'reading', 'learn', 'education',
    'children', 'kids', 'story', 'book', 'biff', 'chip', 'kipper', 'floppy'
]

NEGATIVE_KEYWORDS = [
    'scary', 'violent', 'inappropriate', 'adult', 'horror', 'fight'
]

TRUSTED_CHANNEL_INDICATORS = [
    'oxford owl', 'oxford university press', 'collins big cat',
    'phonics with', 'reading eggs', 'learn with', 'education'
]

# 적절한 영상 길이 (초 단위)
MIN_VIDEO_DURATION = 60    # 1분
MAX_VIDEO_DURATION = 1200  # 20분

