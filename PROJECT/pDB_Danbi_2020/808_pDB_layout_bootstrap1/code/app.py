from flask import Flask, render_template, request, url_for
import pandas as pd
import danbi
import sys

# Initialize
app = Flask(__name__, static_folder='static')
## no cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.after_request
def set_response_headers(r):
    r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    return r

### top-level
# Define a route for url
@app.route('/index')
def index():
    danbi.make_cloud_image()
    return render_template("index.html")

### web menu
##01-01 태그기반 유사동영상 검색 페이지
@app.route('/web_search_similar_video')
def web_search_similar_video():
    return render_template('web_search_similar_video.html')
#########################이 부분도 일형 수정###################################
##01-01 태그기반 유사동영상 검색 결과 페이지
@app.route('/sim_video_css', methods = ['POST', 'GET'])
def sim_video_css():
    if request.method == 'POST':
        keyword_str = request.form['input']
        print(keyword_str)
        std_video_df = danbi.get_video_by_keyword(keyword_str,4)
        print(std_video_df)
        if len(std_video_df) != 0:
            sim_video_df = danbi.get_sim_video_for_web(std_video_df)
#            print(sim_video_df)
        ##여기 수정했음
        elif len(std_video_df) == 0:
            return render_template("no_data.html")
            #해결!
        else:
            sim_video_df = 0
#            print('sim' + str(sim_video_df))
        print(sim_video_df)
        return render_template("sim_video_css.html",
                               std_video_cnt = len(std_video_df),
                               std_video_df=std_video_df,
                               keyword = keyword_str,
                               sim_video_df=sim_video_df)
#############################여기서부터 내가 쓰는 함수#############################################################
##01-02 불법유사 콘텐츠 검색 페이지
@app.route('/copyright_home')
def copyright_home():
    today_str = danbi.get_today_str()
    video_cnt = danbi.get_same_video_search_cnt()
    video_today_cnt = danbi.get_same_video_search_today_cnt()
    same_video_df = danbi.get_new_same_video_list()
    youtube_ids = same_video_df['youtube_id'].to_list()
    titles = same_video_df['title'].to_list()
    dates = same_video_df['insert_date'].to_list()
    same_video_info = zip(youtube_ids, titles, dates)
    
    return render_template('copyright_home.html',
                            video_cnt = video_cnt,
                            video_today_cnt = video_today_cnt,
                            today_str = today_str,
                            same_video_info = same_video_info) 


##01-02 불법유사 콘텐츠 검색 결과 - 아이디 검색 결과
@app.route('/copyright_result', methods=['POST', 'GET'])
def copyright_result():
    if request.method == 'POST':
        print('copyright_result page')
        result_dict = request.form
        ##search_video_keyword = result_dict['imgbase_search_videoid']
        vid = result_dict['imgbase_search_videoid']
        yid = result_dict['imgbase_search_youtubeid']
        ##아래 수정
        #youtube_id = result_dict['youtube_id']
        print('print id') 
        print(vid)
        print(yid)
        # 아래 수정
        #print('youtube_id') 
        #print(youtube_id) 
        
        cnt = 10
        ## video_info, video_cnt = danbi.imgbase_search_sim_video_info(search_video_keyword, search_youtubeid)
        video_info, video_cnt = danbi.imgbase_search_sim_video_info2(vid, yid, cnt)
        if video_cnt > 0:
            return render_template("copyright_result.html",
                                   search_video_keyword = vid,
                                   search_youtubeid = yid,
                                   std_sim_video_info = video_info,
                                   video_cnt = video_cnt) #여기 수정
                                
        else:
            # return "유사 동영상이 없습니다. 이전으로 되돌아 가서 다시 검색하세요"
            return render_template('no_data.html')

##01-02불법유사 콘텐츠 검색 결과 - 전체보기
@app.route('/copyright_result_showall', methods=['POST', 'GET'])
def copyright_result_showall():
    img_dissimilarity = 0.01
    tag_sim = 0.05
    std_sim_video_info, video_cnt = danbi.imgbase_show_all_info(img_dissimilarity, tag_sim)

    if video_cnt > 0:
        return render_template("copyright_result.html",
                               search_video_keyword="전체동영상",
                               search_youtubeid = "전체동영상",
                               std_sim_video_info=std_sim_video_info,
                               video_pair_cnt=video_cnt)
    else:
        return render_template('no_data.html')
        # return "유사 동영상이 없습니다. 이전으로 되돌아 가서 다시 검색하세요"
        # 클릭하면 전체페이지를 보는 부분이라 안고쳐도 될거 같지만 고쳐놓앗습니다.
       

###################################1차 여기까지###############################################################

##01-03 빅데이터 가시화 테스트
@app.route('/wordcloud_img')
def wordcloud_img():
    return render_template("wordcloud_img.html")

##01-04 사용자설문조사 테스트
## CLICK 버튼 누르면 다시 해당페이지에 다른 동영상이 게시되면서 새로운 설문조사 요청 나타남
@app.route('/user_sim_survey', methods=['POST','GET'])
def user_sim_survey():

    if request.method == 'POST':
        youtube_id = request.form['youtube_id']
        score = request.form['score']
        print(youtube_id)
        print(score)

        danbi.survey_add_score(youtube_id, score)
        
        vote_total_cnt, vote_good_cnt = danbi.get_survey_score()
        youtube_id, title, tag = danbi.get_1_video()
        score = round(vote_good_cnt / vote_total_cnt, 4) * 100

        #return "hi"
        ##return redirect('user_sim_survey.html')

        return render_template('user_sim_survey.html',
                           vote_total_cnt = vote_total_cnt,
                           vote_good_cnt = vote_good_cnt,
                           score = score,
                           youtube_id = youtube_id,
                           title = title,
                           tag = tag)

        ## 비디오아이디와 스코어를 DB에 업로드 하는 함수
    else:
        vote_total_cnt, vote_good_cnt = danbi.get_survey_score()
        youtube_id, title, tag = danbi.get_1_video()
        score = vote_good_cnt / vote_total_cnt * 100

        #return "hi"
        ##return redirect('user_sim_survey.html')

        return render_template('user_sim_survey.html',
                           vote_total_cnt = vote_total_cnt,
                           vote_good_cnt = vote_good_cnt,
                           score = score,
                           youtube_id = youtube_id,
                           title = title,
                           tag = tag)
        # return "FAIL"

### mobile
##02-01 태그기반 유사동영상 검색(미측정) - 검색페이지
@app.route('/mobile_search_similar_notime')
def mobile_search_similar_notime():
    return render_template('mobile_search_similar_notime.html')

##02-01 태그기반 유사동영상 검색(미측정) - 기준동영상 검색결과 페이지

@app.route('/mobile_search_result_notime', methods=['POST', 'GET'])
def mobile_search_result_notime():
    keyword_str=request.form['mobile_search_keyword']
    std_video_info, video_cnt = danbi.get_video_info_by_keyword(keyword_str, 4)
    print(keyword_str)
    print(video_cnt)
                              
    if video_cnt == 0:
        # return "검색 결과가 없습니다. 돌아가서 다른 검색어를 넣어주세요"
        ###이 부분 수정
        return render_template("no_data.html")
    else:
        return render_template('mobile_search_result_notime.html',
                               keyword_str=keyword_str,
                               std_video_info=std_video_info
                               )

##02-01 태그기반 유사동영상 검색(미측정) - 유사동영상 검색결과 페이지
@app.route('/mobile_sim_result_notime', methods=['POST', 'GET'])
def mobile_sim_result_notime():
    if request.method == 'POST':
        std_video_id=request.form['std_video_id']
        print(std_video_id)
        ##기준동영상
        std_youtube_id, std_title=danbi.get_video_info_from_video_id(std_video_id)

        ##유사동영상
        sim_video_df=danbi.get_sim_video_for_mobile(std_video_id)
        print(sim_video_df)
        sim_video_df=sim_video_df[:4]

        sim_video_cnt=len(sim_video_df)
        print(sim_video_cnt)

        ids=sim_video_df['video_id'].to_list()
        titles=sim_video_df['title'].to_list()
        youtube_ids=sim_video_df['youtube_id'].to_list()
        sims=sim_video_df['sim'].to_list()
        sim_video_info=zip(youtube_ids, titles, sims, ids)

        return render_template("mobile_sim_result_notime.html",
                               std_video_id=std_video_id,
                               std_youtube_id=std_youtube_id,
                               std_title=std_title,
                               sim_video_info=sim_video_info,
                               sim_video_cnt=sim_video_cnt
                               )


##02-03 불법유사동영상 검색 페이지
@app.route('/imgbase_search')
def imgbase_search():
    return render_template('imgbase_search.html')


#######웹 페이지에서 /imgbase_html을 사용하지 않는거 같습니다.
##02-03 불법유사동영상 검색 결과페이지
@app.route('/imgbase_show_all', methods=['POST', 'GET'])
def imgbase_show_all():
    img_dissimilarity = 0.015
    tag_sim = 0.5
    std_sim_video_df = danbi.imgbase_show_all(img_dissimilarity, tag_sim)
    video_pair_cnt = len(std_sim_video_df)
    
    if video_pair_cnt > 0:
        videoid01s = std_sim_video_df['videoid1'].to_list()
        youtubeid01s = std_sim_video_df['youtubeid1'].to_list()
        videoid02 = std_sim_video_df['videoid2'].to_list()
        youtubeid02s = std_sim_video_df['youtubeid2'].to_list()
        v1_start_times = std_sim_video_df['v1_start_time'].to_list()
        v1_end_times = std_sim_video_df['v1_end_time'].to_list()
        v2_start_times = std_sim_video_df['v2_start_time'].to_list()
        v2_end_times = std_sim_video_df['v2_end_time'].to_list()
        sims = std_sim_video_df['sim'].to_list()
        title01s = std_sim_video_df['title01'].to_list()
        title02s = std_sim_video_df['title02'].to_list()

        std_sim_video_info = zip(videoid01s,
                                 youtubeid01s,
                                 videoid02,
                                 youtubeid02s,
                                 v1_start_times,
                                 v1_end_times,
                                 v2_start_times,
                                 v2_end_times,
                                 sims,
                                 title01s,
                                 title02s)
        return render_template("imgbase_keyword_search.html",
                               search_video_keyword="전체동영상",
                               search_youtubeid = "전체동영상",
                               std_sim_video_info=std_sim_video_info,
                               video_pair_cnt=video_pair_cnt)
    else:
        return "유사 동영상이 없습니다. 이전으로 되돌아 가서 다시 검색하세요"
###############위 주석에 설명###########
##02-04태그기반 유사동영상 검색 페이지
@app.route('/mobile_search_similar_video')
def mobile_search():
    return render_template('mobile_search_similar_video.html')

# form action
@app.route('/mobile_search_result', methods=['POST'])
def mobile_search_result():
    print('mobile_search_result')
    keyword_str=request.form['mobile_search_keyword']
    print(keyword_str)
    std_video_df=danbi.get_video_by_keyword(keyword_str, 4)
    print(std_video_df)

    youtube_ids=std_video_df['youtube_id'].to_list()
    titles=std_video_df['title'].to_list()
    video_ids=std_video_df['video_id'].to_list()
    std_video_info=zip(youtube_ids, titles, video_ids)

    if len(std_video_df) == 0:
        print(" std_video_df == 0")
        # return "검색 결과가 없습니다. 돌아가서 다른 검색어를 넣어주세요"
        return render_template("no_data.html")

    else:
        return render_template('mobile_search_result.html',
                                keyword_str=keyword_str,
                                std_video_info = std_video_info
                               )
    
##02-04 태그기반 유사동영상 검색 결과 페이지
@app.route('/mobile_sim_result', methods=['POST', 'GET'])
def mobile_sim_result():
    if request.method == 'POST':
        std_video_id = request.form['std_video_id']
        print(std_video_id)
        time_str = request.form['time_str_name']
        print(time_str)
        time_str = time_str.split("-")
        min_str = time_str[0]
        sec_str = time_str[1]
        print(min_str)
        print(sec_str)

        print(std_video_id)

        ##기준동영상
        std_youtube_id, std_title = danbi.get_video_info_from_video_id(std_video_id)
        print(std_youtube_id)
        print(std_title)

        ##유사동영상
        print("유사동영상")
        sim_video_df = danbi.get_sim_video_for_mobile(std_video_id)
        print(sim_video_df)
        sim_video_df = sim_video_df[:4]


        sim_video_cnt = len(sim_video_df)
        print(sim_video_cnt)

        ids = sim_video_df['video_id'].to_list()
        titles = sim_video_df['title'].to_list()
        youtube_ids = sim_video_df['youtube_id'].to_list()
        sims = sim_video_df['sim'].to_list()
        sim_video_info = zip(youtube_ids, titles, sims, ids)

        return render_template("mobile_sim_result.html",
                               std_video_id=std_video_id,
                               std_youtube_id=std_youtube_id,
                               std_title=std_title,
                               sim_video_info=sim_video_info,
                               sim_video_cnt=sim_video_cnt,
                               min_str=min_str,
                               sec_str=sec_str
                               )


### 03 기타(미사용) 

'''
#@app.route('/imganal_search')
#def imganal_search():
#    return render_template('imganal_search.html')


@app.route('/imgbase_keyword_search', methods=['POST', 'GET'])
def imgbase_keyword_search():
    print('mobile_keyword_search_result')
    if request.method == 'POST':
        result_dict=request.form
        search_video_keyword=result_dict['imgbase_search_videoid']
        search_video_id=result_dict['imgbase_search_videoid']        

        print(search_video_keyword)
        print(search_youtubeid)

        video_info, video_cnt = danbi.imgbase_search_sim_video_info(search_video_keyword, search_youtubeid)
        print(video_cnt)
        print(video_info)
        if video_cnt > 0:
            return render_template("imgbase_keyword_search.html",
                                   search_video_keyword=search_video_keyword,
                                   search_youtubeid = search_youtubeid,
                                   std_sim_video_info = video_info,
                                   video_cnt = video_cnt)
        else:
            return "유사 동영상이 없습니다. 이전으로 되돌아 가서 다시 검색하세요"

'''
#연습용 페이지를 만들어 보자.
@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/test_result', methods=['POST'])
def test_result():
    keyword_str=request.form['imgbase_search_videoid']
    print(keyword_str)

    return render_template("test_result.html")

###jih flask_bootstraptest

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/sidenav')
def sidenav():
      return render_template('sidenav.html')

@app.route('/about')
def about():
  return render_template('about.html')



# Run the app
if __name__=='__main__':
    app.run(host='0.0.0.0', port= 5000, debug=True)
