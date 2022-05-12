from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for,Blueprint
from datetime import datetime, timedelta

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.cracker

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
app.config['UPLOAD_FOLDER'] = "./static/marker_pics"

SECRET_KEY = 'Cracker'

bp = Blueprint('auth', __name__)

@bp.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_mail": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.login", msg="로그인 정보가 존재하지 않습니다."))

@bp.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@bp.route('/sign_in', methods=['POST'])
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


@bp.route('/sign_up/save', methods=['POST'])
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
        "user_info": "" ,                                         # 프로필 한 마디
        "marker_pic":"",
        "marker_pic_real": "marker_pics/marker-default.png"
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@bp.route('/sign_up/check_email_dup', methods=['POST'])
def check_email_dup():
    user_mail_receive = request.form['user_mail_give']
    exists = bool(db.users.find_one({"user_mail": user_mail_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@bp.route('/sign_up/check_user_dup', methods=['POST'])
def check_user_dup():
    user_name_receive = request.form['user_name_give']
    exists = bool(db.users.find_one({"user_name": user_name_receive}))
    return jsonify({'result': 'success', 'exists': exists})