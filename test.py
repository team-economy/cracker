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


@app.route("/get_posts", methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        my_user_name = payload["id"]
        # user_name_receive = request.args.get("user_name_give")
            #date 내림차순 (최근것부터).20개 한정
        # if user_name_receive == "":
        #     posts = list(db.posts.find({}).sort("date", -1).limit(20))
        # else:
        #     posts = list(db.posts.find({"user_name": user_name_receive}).sort("date", -1).limit(20))
        posts = list(db.posts.find({},{'_id': False}).sort("date", -1))
        print(posts)
            #좋아요 고유식별자
        # for post in posts:
        #     post["_id"] = str(post["_id"])
        #
        #     post["count_like"] = db.likes.count_documents({"post_id": post["_id"], "type": "like"})
        #     post["like_by_me"] = bool(
        #         db.likes.find_one({"post_id": post["_id"], "type": "like", "user_name": my_user_name}))
        #
        #     post["count_unlike"] = db.likes.count_documents({"post_id": post["_id"], "type": "unlike"})
        #     post["unlike_by_me"] = bool(
        #         db.likes.find_one({"post_id": post["_id"], "type": "unlike", "user_name": my_user_name}))

        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "posts": posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 좋아요 수 변경
        user_info = db.users.find_one({"user_mail": payload["id"]})
        post_id_receive = request.form["post_id_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        doc = {
            "post_id": post_id_receive,
            "user_name": user_info["user_name"],
            "type": type_receive
        }
        if action_receive =="like":
            db.likes.insert_one(doc)
        else:
            db.likes.delete_one(doc)
        count = db.likes.count_documents({"post_id": post_id_receive, "type": type_receive})
        print(count)
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/delete", methods=['DELETE'])
def delete_date():
    token_receive = request.cookies.get('mytoken')
    try:
        # user 정보
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_mail": payload["id"]})

        commu_receive = request.form['commu_give']

        saved_date = db.posts.find_one({'date': commu_receive})

        if (user_info["user_mail"] == saved_date["user_mail"] and user_info["user_name"] == saved_date[
            "user_name"]):
            db.posts.delete_one({'date': commu_receive})
            return jsonify({'result': 'success', 'msg': '삭제 완료!!'})
        else:
            return jsonify({'result': 'success', 'msg': '계정 정보를 확인하세요.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
