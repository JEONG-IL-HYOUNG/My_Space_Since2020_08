import os
import pandas as pd
import sys
import oaislib
import shutil
import youtube_dl
import time

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')

### 10개까지만의 동영상을 다운로드 받도록 함
## 다운로드 받을 동영상이 없으면 1시간 대기 

def ps3010(dn_num): #한번에 받을 동영상 수 제한
    ### IO name
    ## input
    input_filepath = 'output/ps2050/youtube_tbl.csv'
    y_df = pd.read_csv(input_filepath)
    prefix = 'ps3010'

    ## output
    output_filepath = 'output/ps3010/01_y_tbl_dn.csv'

    ### data load
    today_str = oaislib.fn_get_date_str()
    input_df = pd.read_csv(input_filepath)

    output_new_df = input_df.copy()
    output_new_df['dn_yn'] = ""
    output_new_df['dn_date'] = ""
    

    ### 업데이트된 리스트를 불러온 후에 거기에 기존 다운로드 정보를 덮어씌운다.
    if os.path.exists(output_filepath):
        output_old_df = pd.read_csv(output_filepath)
        output_old_df = output_old_df[output_old_df.dn_yn == "y"]
        output_old_cnt = len(output_old_df)

        for i in range(output_old_cnt):
            yid_str = output_old_df['yid'].iloc[i]
            date_str = output_old_df['udate'].iloc[i]
            output_new_df.dn_yn.loc[output_new_df.yid == yid_str] = 'y'
            output_new_df.dn_date.loc[output_new_df.yid == yid_str] = date_str

    ### 동영상 다운로드 받음
    output_new_cnt = len(output_new_df)

    ### 다운로드 경로 및 파일명 지정
    video_download_path = './output/ps3010'  # 다운로드 경로
    download_path = os.path.join(video_download_path, '%(id)s.%(ext)s')

    idx_dn = 0
    for i in range(output_new_cnt):

        dn_yn_str = output_new_df.dn_yn.iloc[i]

        if dn_yn_str != 'y':
            y_url =  output_new_df.y_url.iloc[i]
            ydl_opts = {
                'format': '135[ext=mp4]/best[height<=360 ext=mp4]',  # (화질을 선택하여 다운로드 가능)
                'outtmpl': download_path # 다운로드 경로 설정
            }
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    rlt_message = ydl.download([y_url])
                    print("success", rlt_message)
                    output_new_df['dn_yn'].iloc[i] = "y"
                    output_new_df['dn_date'].iloc[i] = today_str
                    oaislib.fn_disploop(prefix, idx_dn, 1, dn_num)
                    idx_dn = idx_dn + 1
                    time.sleep(5)

            except Exception as e:
                output_new_df['dn_yn'].iloc[i] = "f"
                print('error!!!!!', e)

        if idx_dn > dn_num:
            break

    ## 신규 다운로드 항목이 없는 경우 반복문을 위한 시간 딜레이
    if idx_dn == 0:
        print('url for downloading is zero')
        time.sleep(60*60*2)
        sys.exit()

    output_new_df.to_csv(output_filepath, index=False)

if __name__ == "__main__":
    ps3010(10) # 10개까지만의 동영상을 다운로드 받도록 함
    breakpoint()
