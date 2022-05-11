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

# 사용자페이지
@app.route('/user/<user_mail>')
def user(user_mail):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (user_mail == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
        user_info = db.users.find_one({"user_mail":user_mail}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# 사용자페이지 - 프로필 사진 업로드
@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_mail = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]
        new_doc = {
            "user_name": name_receive,
            "user_info": about_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{user_mail}.{extension}"
            file.save("./static/"+file_path)
            new_doc["user_pic"] = filename
            new_doc["user_pic_real"] = file_path
        db.users.update_one({'user_mail': payload['id']}, {'$set':new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# 사용자페이지 - 마커 사진 업로드
@app.route('/update_marker', methods=['POST'])
def save_marker():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_mail = payload["id"]

        new_doc = {
        }

        if 'marker_give' in request.files:
            marker = request.files["marker_give"]
            marker_name = secure_filename(marker.filename)
            extension = marker_name.split(".")[-1]
            marker_path = f"marker_pics/{user_mail}.{extension}"
            marker.save("./static/"+marker_path)
            new_doc["marker_pic"] = marker_name
            new_doc["marker_pic_real"] = marker_path
            print(new_doc)
        db.users.update_one({'user_mail': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success", 'msg': '마커 이미지를 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

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
