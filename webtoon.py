import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.itbv7ku.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.xevhlvh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

from selenium import webdriver

import datetime
import time
import json

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
app = Flask(__name__)
app.secret_key = "My_Key"
app.permanent_session_lifetime = datetime.timedelta(minutes=30)

from pymongo import MongoClient
import certifi

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


# 코딩 시작
# ------------네이버
data_naver = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bjQz&pkid=47&qvt=0&query=%EC%A3%BC%EA%B0%84%20%EB%9E%AD%ED%82%B9%20%EC%9B%B9%ED%88%B0',headers=headers)
soup_naver = BeautifulSoup(data_naver.text, 'html.parser')
naver_webtoon_card = soup_naver.select('#mflick > div > div > ul > li')
db.naver_webtoon.drop()

for naver_webtoon in naver_webtoon_card:
    a = naver_webtoon.select_one('div > a > div')
    if a is not None:
        rank = a.text
        title = naver_webtoon.select_one('div > div > strong > a').text
        sub_title = naver_webtoon.select_one('div > div > span').text
        image = naver_webtoon.select_one('div > a > div > img')['src']
        url = "https://comic.naver.com/webtoon/list?titleId=" + str(naver_webtoon.select_one('div > a > div > img')).split('webtoon%2F')[1].split('%')[0]

        # print(url1)
        # url = "https://search.naver.com/search.naver" + naver_webtoon.select_one('div > a')['href']
        doc = {
            'rank':rank,
            'title':title,
            'sub_title':sub_title,
            'image':image,
            'url':url
        }
        db.naver_webtoon.insert_one(doc)

# ------------카카오
data_kakao = requests.get('https://page.kakao.com/menu/10/screen/6?subcategory_uid=0&ranking_type=monthly',headers=headers)
soup_kakao = BeautifulSoup(data_kakao.text, 'html.parser')
kakao_webtoon_card = soup_kakao.select('#__next > div > div.css-gqvt86-PcLayout > div > div.css-1dqbyyp-Home > div.css-z5atxi > div > div.css-1k8yz4-StaticLandingRanking > div > div > div > div')
db.kakao_webtoon.drop()
for kakao_webtoon in kakao_webtoon_card:
    b = kakao_webtoon.select_one('div > div > a > div > div.css-x5ksav-NormalListViewItem > span.css-19hzfyp-Text-NormalListViewItem')
    if b is not None:
        rank = b.text
        title = kakao_webtoon.select_one('div > div > a > div > div.css-x5ksav-NormalListViewItem > span.css-mmgb7c-Text-NormalListViewItem').text
        sub_title = kakao_webtoon.select_one('div > div > a > div > div.css-x5ksav-NormalListViewItem > div ').text
        if "억" in sub_title:
            sub_title = sub_title.split('억')[1].split(',')[0]
        else:
            sub_title = sub_title.split('만')[1].split(',')[0]
        image = kakao_webtoon.select_one('div > div > a > div > div.css-ne1sxt-ThumbnailWithBadges-NormalListViewItem > div.css-13oqwjg-Image-ThumbnailWithBadges > img')['src']
        url = "https://page.kakao.com" + kakao_webtoon.select_one('div > div > a')['href']
        doc = {
            'rank': int(rank),
            'title': title,
            'sub_title': sub_title,
            'image': image,
            'url': url
        }

        db.kakao_webtoon.insert_one(doc)

# ------------레진
# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# driver = webdriver.Chrome(options=options)
# driver.get("https://www.lezhin.com/ko/ranking/detail?genre=_all&type=realtime")
# html = driver.page_source
# soup_lezhin = BeautifulSoup(html,"html.parser")
#
# items = soup_lezhin.select(".lzComic__link")
#
# # print(items)
# db.lezhin_webtoon.drop()
# count = 0
# for lezhin_webtoonm, item in enumerate(items, 1):
#
#     title = str(item.select_one(".lzComic__title")).split('</span>')[1].split('<')[0].strip()
#     sub_title = item.select_one(".lzComic__artist").text
#     rank = item.select_one(".lzComic__rank").text
#     image = str(item.select_one(".lzComic__img")).split('t="')[1].split('"')[0]+"0"
#     url = "https://www.lezhin.com/" + str(item).split('href="')[1].split('"')[0]
#     doc = {
#         'rank': rank,
#         'title': title,
#         'sub_title': sub_title,
#         'image': image,
#         'url': url
#     }
#     db.lezhin_webtoon.insert_one(doc)
#     count +=1
#     if count == 18:
#         break
# driver.quit()

# ---------------------------------------------------


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        pw_again_receive = request.form['pw_again_give']
        name_receive = request.form['name_give']
        address_receive = request.form['address_give']
        email_receive = request.form['email_give']

        if name_receive == "" or address_receive == "":
            return jsonify({'msg': '빈칸을 채워주세요 !'})


            if db.user.find_one({'id': id_receive}):
                return jsonify({'msg': '동일한 아이디가 존재합니다 !'})
            elif id_receive == "":
                return jsonify({'msg': '아이디를 입력해주세요 !'})
            elif pw_receive == "":
                return jsonify({'msg': '비밀번호를 입력해주세요 !'})



        else:
            if pw_receive == pw_again_receive:
                session['id'] = id_receive
                session['pw'] = pw_receive
                doc = {
                    'id': id_receive,
                    'pw': pw_receive,
                    'name' : name_receive,
                    'address' : address_receive,
                    'email' : email_receive
                }
                db.user.insert_one(doc)
                return jsonify({'msg': '회원가입을 축하합니다 !'})
            else:
                return jsonify({'msg': '비밀번호가 일치하지 않습니다 !'})
        return render_template("index.html")
    else:
        return render_template("signup.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']


        if db.user.find_one({'id':id_receive}): # DB안에 login.html의 ID 입력값 유무 확인
            session['id'] = id_receive  # 있을시 session에 값 입력
            if db.user.find_one({'pw': pw_receive}):  # DB안에 login.html의 PW 입력값 유무 확인
                session['pw'] = pw_receive  # 있을시 session에 값 입력
                return jsonify({'msg': '로그인에 성공하였습니다 !'})
            else:
                return jsonify({'msg': '비밀번호가 틀렸습니다 !'})
        else:
            return jsonify({'msg': '동일한 아이디가 존재하지 않습니다 !'})

        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect('/')

@app.route('/myinfo_data', methods=["GET"])
def info():
    info_list = list(db.user.find({}, {'_id': False}))
    return jsonify({'lists': info_list})


@app.route('/myinfo')
def info2():
    return render_template('myinfo.html')

# --------------------------------------

@app.route('/')
def index():
    if 'id' in session: # 세션안에 id가 있을경우
        if 'pw' in session: # 세션안에 id가 있을경우 + 세션안에 pw가 있을경우
            id = session['id']
            pw = session['pw']
            return render_template("index_success_login.html") # session안에 데이터가 있을때
        else:
            return render_template("index.html") # session안에 데이터가 없을때
    else:
        return render_template("index.html") # session안에 데이터가 없을때

@app.route('/suzy')
def getsuzy():
    return render_template('suzy.html')

@app.route('/index_success_login')
def getindex_success_login():
    return render_template('index_success_login.html')

@app.route('/login')
def getlogin():
    return render_template('login.html')

@app.route('/myinfo')
def getmyinfo():
    return render_template('myinfo.html')

@app.route('/signup')
def getsignup():
    return render_template('signup.html')

@app.route("/naver_webtoon", methods=["GET"])
def naver_webtoon_get():
    all_naver_webtoon = list(db.naver_webtoon.find({}, {'_id': False}))
    return jsonify({'naver_webtoons': all_naver_webtoon})

@app.route("/kakao_webtoon", methods=["GET"])
def kakao_webtoon_get():
    all_kakao_webtoon = list(db.kakao_webtoon.find({}, {'_id': False}))
    return jsonify({'kakao_webtoons': all_kakao_webtoon})

@app.route("/lezhin_webtoon", methods=["GET"])
def lezhin_webtoon_get():
    all_lezhin_webtoon = list(db.lezhin_webtoon.find({}, {'_id': False}))
    return jsonify({'lezhin_webtoons': all_lezhin_webtoon})

@app.route("/board")
def board_html():
    if 'id' in session:
        if 'pw' in session:
            return render_template("board.html")  # 아이디 비밀번호가 있을때
    else:
        return render_template("index.html") # 아이디 혹은 비밀번호가 없을떄

@app.route("/board/get", methods= ["GET"])
def board_get():
    board_list = list(db.board.find({}, {'_id': False}))

    return jsonify({'boards': board_list})



@app.route('/board/post', methods = ['POST'])
def board_POST():
    # board DB에 들어갈 데이터 목록 -------------------------------
    # number_receive    글번호         app.py에서 구현
    # title_receive     제목          html에서 받아옴
    # contents_receive  내용          html에서 받아옴
    # name_receive      이름(아이디X)   app.py에서 구현
    # date_receive      등록일         app.py에서 구현
    # ------------------------------------- ----------------

    # number_receive 구현 ------------------------------------
    board_list = list(db.board.find({}, {'_id': False}))
    count = len(board_list) + 1
    # -------------------------------------------------------

    # name_receive 구현 -------------------------------------
    user_list = list(db.user.find({}, {'_id': False}))
    cnt = len(user_list)
    sessionID = session['id']
    name = ''

    for i in range(cnt):
        if user_list[i]['id'] == sessionID:
            name = user_list[i]['name']
    # ------------------------------------------------------

    # date_receive 구현 -------------------------------------
    now = time
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    # ------------------------------------------------------

    # board DB에 데이터 등록 ------------------------------------
    number_receive = count
    title_receive = request.form['title_give']
    contents_receive = request.form['contents_give']
    boardurl_reveive = request.form['boardurl_give']
    name_receive = name
    date_receive = date

    doc = {
        'number': number_receive,
        'title': title_receive,
        'contents': contents_receive,
        'name': name_receive,
        'date': date_receive,
        'boardurl': boardurl_reveive
    }
    db.board.insert_one(doc)
    # -------------------------------------------------------

    return jsonify({'msg':'등록 완료 !'})

@app.route("/board_write")
def board_write_html():
    return render_template("board_write.html")

@app.route("/board_view")
def board_view_html():
    return render_template("board_view.html")

@app.route("/board_view/get", methods= ["GET"])
def board_view_get():
    board_list = list(db.board.find({}, {'_id': False}))

    return jsonify({'boards': board_list})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)