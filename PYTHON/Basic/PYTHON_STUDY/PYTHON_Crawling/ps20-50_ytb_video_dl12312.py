import youtube_dl
import os
#test
#여기라인에서 인풋으로 유튜브 아이디 불러오기
#down_url = "https://www.youtube.com/watch?v=" + youtube_id
#filname = youtube_id + '.mp4'
#print('video is downloading....'+'url :' + down_url)
#run_text = ['youtube-dl', down_url, '-f', 'mp4', '-o', '01_mov/' + filname]
#down_rlt = subprocess.call(run_text)

VIDEO_DOWNLOAD_PATH = './output/ps20-50'  # 다운로드 경로

def download_video_and_subtitle(output_dir, youtube_video_list):

    download_path = os.path.join(output_dir, '%(id)s-%(title)s.%(ext)s')

    for video_url in youtube_video_list:
        # youtube_dl options
        ydl_opts = {
            'format': 'best[height<=480]',  # (화질을 선택하여 다운로드 가능)
            'outtmpl': download_path, # 다운로드 경로 설정
            'writesubtitles': 'best', # 자막 다운로드(자막이 없는 경우 다운로드 X)
            'writethumbnail': 'best',  # 영상 thumbnail 다운로드
            'writeautomaticsub': True, # 자동 생성된 자막 다운로드
            'subtitleslangs': 'en'  # 자막 언어가 영어인 경우(다른 언어로 변경 가능)

        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception as e:
            print('error', e)

if __name__ == '__main__':

    youtube_url_list = [  # 유투브에서 다운로드 하려는 영상의 주소 리스트(아래는 Sample Video 리스트)
        "https://www.youtube.com/watch?v=CKVe4LzDOXo",
        "https://www.youtube.com/watch?v=3VTkBuxU4yk",
        "https://www.youtube.com/watch?v=MmlzoB0WC4s",
        "https://www.youtube.com/watch?v=ufupPuN8VVw"
    ]
    download_video_and_subtitle(VIDEO_DOWNLOAD_PATH, youtube_url_list)
    print('Complete download!')

