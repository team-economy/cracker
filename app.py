from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.cracker

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'Cracker'


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    print(token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_mail": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/maps', methods=["GET"])
def get_matjip():
    matjip_list = list(db.matjip.find({}, {"_id": False}))

    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    user_mail_receive = request.form['user_mail_give']
    user_pw_receive = request.form['user_pw_give']

    pw_hash = hashlib.sha256(user_pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'user_mail': user_mail_receive, 'user_pw': pw_hash})

    if result is not None:
        payload = {
         'id': user_mail_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    user_mail_receive = request.form['user_mail_give']
    user_name_receive = request.form['user_name_give']
    user_pw_receive = request.form['user_pw_give']
    password_hash = hashlib.sha256(user_pw_receive.encode('utf-8')).hexdigest()
    doc = {
        "user_mail": user_mail_receive,                               # 이메일
        "user_name": user_name_receive,                               # 프로필 이름
        "user_pw": password_hash,                                  # 비밀번호
        "user_pic": "",                                          # 프로필 사진 파일 이름
        "user_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "user_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    user_mail_receive = request.form['user_mail_give']
    exists = bool(db.users.find_one({"user_mail": user_mail_receive}))
    return jsonify({'result': 'success', 'exists': exists})

# 맛집 검색하면 키워드에 해당하는 목록을 전달
@app.route("/get_address", methods=['GET'])
def get_address():
    place_receive = request.args.get("place_give")
    if(place_receive == ""):
        return({"result":"success", "msg":"input empty"})
    else:
        searching = place_receive
        print (place_receive)
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
        headers = {
            "Authorization": "KakaoAK b2cd5fe8152984068e62cf5b85fbb75a"
        }
        places = requests.get(url, headers = headers).json()['documents']
        print(places)
        if (places == []):
            return({"result":"success", "msg":"no result"})
        else:
            return ({"result":"success", "msg":"good", "places":places})

# 선택한 맛집 DB에 저장
@app.route("/save_place", methods=['POST'])
def save_place():
    place_receive = request.form["place_give"]
    addr_receive = request.form["addr_give"]
    addr_road_receive = request.form["addr_road_give"]
    x_receive = request.form["x_give"]
    y_receive = request.form["y_give"]
    doc = {
        "matjip_name":place_receive,
        "matjip_address":addr_receive,
        "matjip_road_address":addr_road_receive,
        "user_name":'cheoljin',
        "profile_name":'cheoljin',
        "x":x_receive,
        "y":y_receive
    }
    db.matjip.insert_one(doc)
    return({"result":"success"})

# 맛집 DB에서 값을 가져와서 리스트 출력
@app.route('/get_place', methods=["GET"])
def get_place():

    matjip_list = list(db.matjip.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'matjip_list': matjip_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)