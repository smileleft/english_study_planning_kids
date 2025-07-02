from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional
import time
import logging
from datetime import datetime
from ..models.video_model import VideoData
from ..models.channel_model import ChannelData

class YouTubeCollector:
    def __init__(self, api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.logger = logging.getLogger(__name__)
        self.collected_video_ids = set()
    
    def search_videos(self, query: str, max_results: int = 25) -> List[Dict]:
        """키워드로 영상 검색"""
        try:
            self.logger.info(f"검색 시작: '{query}' (최대 {max_results}개)")
            
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                order='relevance',
                videoDuration='medium',  # 4-20분 영상
                videoDefinition='any',
                regionCode='US'  # 영어 콘텐츠 우선
            ).execute()
            
            videos = []
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            
            # 중복 제거
            new_video_ids = [vid for vid in video_ids if vid not in self.collected_video_ids]
            self.collected_video_ids.update(new_video_ids)
            
            if new_video_ids:
                # 영상 상세 정보 가져오기
                video_details = self._get_videos_details(new_video_ids)
                videos.extend(video_details)
            
            self.logger.info(f"수집 완료: {len(videos)}개 영상 (중복 제거 후)")
            return videos
            
        except HttpError as e:
            self.logger.error(f"YouTube API 오류: {e}")
            return []
        except Exception as e:
            self.logger.error(f"예상치 못한 오류: {e}")
            return []
    
    def get_video_details(self, video_id: str) -> Optional[VideoData]:
        """영상 상세 정보 가져오기"""
        try:
            # 한 번에 최대 50개씩 처리
            videos = []
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                
                response = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(batch_ids)
                ).execute()
                
                for item in response['items']:
                    try:
                        video = self._create_video_data(item)
                        if video:
                            videos.append(video)
                    except Exception as e:
                        self.logger.warning(f"영상 데이터 생성 실패 {item['id']}: {e}")
                        continue
            
            return videos
            
        except HttpError as e:
            self.logger.error(f"영상 상세 정보 가져오기 실패: {e}")
            return []
    
    def get_channel_info(self, channel_id: str) -> Optional[ChannelData]:
        """채널 정보 가져오기"""
        try:
            response = self.youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            ).execute()
            
            if not response['items']:
                return None
            
            item = response['items'][0]
            snippet = item['snippet']
            statistics = item['statistics']
            
            return ChannelData(
                channel_id=channel_id,
                channel_name=snippet['title'],
                description=snippet.get('description', ''),
                subscriber_count=int(statistics.get('subscriberCount', 0)),
                video_count=int(statistics.get('videoCount', 0)),
                view_count=int(statistics.get('viewCount', 0)),
                created_at=snippet.get('publishedAt')
            )
            
        except HttpError as e:
            self.logger.error(f"채널 정보 가져오기 실패 {channel_id}: {e}")
            return None
    
    def get_channel_videos(self, channel_id: str, max_results: int = 25) -> List[Dict]:
        """채널의 영상 목록 가져오기"""
        try:
            # 채널의 업로드 플레이리스트 ID 가져오기
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                self.logger.warning(f"채널을 찾을 수 없음: {channel_id}")
                return []
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # 플레이리스트에서 영상 목록 가져오기
            playlist_response = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=max_results
            ).execute()
            
            # Oxford Reading Tree 관련 영상만 필터링
            relevant_video_ids = []
            for item in playlist_response['items']:
                title = item['snippet']['title'].lower()
                description = item['snippet']['description'].lower()
                
                if self._is_ort_related(title, description):
                    video_id = item['snippet']['resourceId']['videoId']
                    if video_id not in self.collected_video_ids:
                        relevant_video_ids.append(video_id)
            
            # 상세 정보 가져오기
            if relevant_video_ids:
                self.collected_video_ids.update(relevant_video_ids)
                return self._get_videos_details(relevant_video_ids)
            
            return []

        except HttpError as e:
            self.logger.error(f"채널 영상 가져오기 실패 {channel_id}: {e}")
            return []

    def _create_video_data(self, item: Dict) -> Optional[VideoData]:
        """YouTube API 응답을 VideoData 객체로 변환"""
        try:
            snippet = item['snippet']
            statistics = item.get('statistics', {})
            content_details = item['contentDetails']
            
            # 필수 필드 확인
            video_id = item['id']
            title = snippet['title']
            channel_id = snippet['channelId']
            
            video_data = VideoData(
                video_id=video_id,
                title=title,
                description=snippet.get('description', ''),
                channel_id=channel_id,
                channel_title=snippet['channelTitle'],
                published_at=datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')),
                duration=content_details['duration'],
                view_count=int(statistics.get('viewCount', 0)),
                like_count=int(statistics.get('likeCount', 0)),
                comment_count=int(statistics.get('commentCount', 0)),
                thumbnail_url=snippet.get('thumbnails', {}).get('medium', {}).get('url'),
                url=f"https://www.youtube.com/watch?v={video_id}"
            )
            
            return video_data
            
        except Exception as e:
            self.logger.error(f"VideoData 생성 실패: {e}")
            return None
