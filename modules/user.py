from pymongo import MongoClient
import jwt
from flask import Flask, jsonify, request, redirect, url_for, Blueprint, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.cracker
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'Cracker'

bp = Blueprint('user', __name__, url_prefix='/user')

# 사용자페이지
@bp.route('/<user_mail>')
def user(user_mail):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (user_mail == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
        user_info = db.users.find_one({"user_mail":user_mail}, {"_id": False})
        print(status)
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# 사용자페이지 - 프로필 사진 업로드
@bp.route('/update_profile', methods=['POST'])
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
@bp.route('/update_marker', methods=['POST'])
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
        db.users.update_one({'user_mail': payload['id']}, {'$set': new_doc})
        db.matjip.update_one({'user_mail': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success", 'msg': '마커 이미지를 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# 사용자가 저장한 맛집 링크 불러오기
@bp.route('/place', methods=["GET"])
def get_place():
    user_mail_receive = request.args.get("user_mail_give")
    user_place = list(db.matjip.find({"user_mail":user_mail_receive}, {'_id': False}))
    return jsonify({'result': 'success', 'user_place': user_place})