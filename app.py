from flask import Flask

from modules import auth, place, map, blog
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from datetime import datetime, timedelta

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.cracker
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'Cracker'

app.register_blueprint(auth.bp)
app.register_blueprint(place.bp)
app.register_blueprint(map.bp)
app.register_blueprint(blog.bp)


@app.route('/community')
def community():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_mail": payload["id"]})
        return render_template('community.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:  # 유저정보
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_mail": payload["id"]})
        # 포스팅하기
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        print(user_info)
        doc = {
            "user_mail": user_info["user_mail"],
            "user_name": user_info["user_name"],
            "user_pic_real": user_info["user_pic_real"],
            "comment": comment_receive,
            "date": date_receive
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
