import youtube_dl
import os
import pandas as pd

#test
#여기라인에서 인풋으로 유튜브 아이디 불러오기
#down_url = "https://www.youtube.com/watch?v=" + youtube_id
#filname = youtube_id + '.mp4'
#print('video is downloading....'+'url :' + down_url)
#run_text = ['youtube-dl', down_url, '-f', 'mp4', '-o', '01_mov/' + filname]
#down_rlt = subprocess.call(run_text)

input_filepath = 'output/ps20-30/youtube_ids_additional.csv'
youtube_ids_df = pd.read_csv(input_filepath)
video_download_path = './output/ps20-50'  # 다운로드 경로
download_path = os.path.join(video_download_path, '%(id)s.%(ext)s')

youtube_url = youtube_ids_df['youtube_url']
print(type(youtube_url))
print('')

for video_url in youtube_url:
    # youtube_dl options
    ydl_opts = {
        'format': 'best[height<=480]',  # (화질을 선택하여 다운로드 가능)
        'outtmpl': download_path # 다운로드 경로 설정
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        print('error', e)









