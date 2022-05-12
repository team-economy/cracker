from flask import Flask, jsonify, request, redirect, url_for, Blueprint, render_template
from pymongo import MongoClient
import jwt

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.cracker
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'Cracker'

bp = Blueprint('community', __name__, url_prefix='/community')


@bp.route('/<place>')
def user(place):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        place_title = db.matjip.find_one({"matjip_name": place}, {"_id": False})
        user_info = db.users.find_one({"user_mail": payload['id']}, {"_id": False})

        print(place_title)

        return render_template('community.html', user_info=user_info, place_title=place_title)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("auth.home"))

@bp.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user_info = db.users.find_one({"user_mail": payload["id"]})
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        matjip_name_receive = request.form["matjip_name_give"]

        doc = {
            "matjip_name":matjip_name_receive,
            "user_mail": user_info["user_mail"],
            "user_name": user_info["user_name"],
            "user_pic": user_info["user_pic"],
            "user_pic_real": user_info["user_pic_real"],
            "comment": comment_receive,
            "date": date_receive
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@bp.route('/get_post', methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        matjip_name_receive = request.args.get("matjip_name_give")

        posts = list(db.posts.find({"matjip_name": matjip_name_receive}, {'_id': False}))
        return jsonify({'result': 'success', 'posts': posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))