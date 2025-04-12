import yt_dlp
import sys
from urllib.parse import parse_qs, urlparse

def get_video_id(url):
    """YouTube URL에서 비디오 ID를 추출합니다."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
    return None

def download_video(url):
    try:
        video_id = get_video_id(url)
        if not video_id:
            print("올바른 YouTube URL이 아닙니다.")
            return False
            
        print(f"비디오 ID: {video_id}")
        
        ydl_opts = {
            'format': 'best',  # 최고 품질의 동영상 다운로드
            'outtmpl': '%(title)s.%(ext)s',  # 파일 이름 형식
            'progress_hooks': [lambda d: print(f'다운로드 진행률: {d["_percent_str"]}') if d["status"] == "downloading" else None],
            'quiet': False,
            'no_warnings': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 영상 정보 가져오기
            print("영상 정보를 가져오는 중...")
            info = ydl.extract_info(url, download=False)
            print(f"\n제목: {info['title']}")
            print(f"길이: {info['duration']} 초")
            print(f"해상도: {info.get('resolution', 'N/A')}")
            print(f"파일 크기: {info.get('filesize_approx', 'N/A')} bytes\n")
            
            # 다운로드 시작
            print("다운로드를 시작합니다...")
            ydl.download([url])
            
        print("\n다운로드 완료!")
        return True
        
    except Exception as e:
        print(f"다운로드 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        video_url = "https://www.youtube.com/watch?v=9bZkp7q19f0"
    
    download_video(video_url)