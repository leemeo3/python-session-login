import datetime
import json

from flask import Flask, render_template, request, jsonify, session, redirect
app = Flask(__name__)
app.secret_key = "key"
app.permanent_session_lifetime = datetime.timedelta(minutes=10)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.xevhlvh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def index():
    if 'id' in session: # 세션안에 id가 있을경우
        if 'pw' in session: # 세션안에 id가 있을경우 + 세션안에 pw가 있을경우
            return render_template("index_success_login.html") # session안에 데이터가 있을때
        else:
            return render_template("index.html") # session안에 데이터가 없을때
    else:
        return render_template("index.html") # session안에 데이터가 없을때

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
        elif pw_receive =="":
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
            session['id'] = id_receive # 있을시 session에 값 입력
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

@app.route('/change_pw_data', methods = ['GET', 'POST'])
def change_pw():
    sessionId = session['id']
    current_pw_receive = request.form['current_pw_give']
    new_pw_receive = request.form['new_pw_give']
    new_pw_again_receive = request.form['new_pw_again_give']

    if current_pw_receive != session['pw']:
        return jsonify({'msg': '현재 비밀번호가 틀렸습니다 !'})
    if new_pw_receive != new_pw_again_receive:
        return jsonify({'msg': '비밀번호가 다릅니다 !'})
    else:
        db.user.update_one({'id': sessionId}, {'$set': {'pw': new_pw_receive}})
        session.clear()
        return jsonify({'msg': '새로운 비밀번호로 로그인하세요 !'})
    return render_template("index.html")

@app.route('/change_pw')
def info3():
    return render_template('change_pw.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)