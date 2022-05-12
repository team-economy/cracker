from pymongo import MongoClient
import jwt
from flask import Flask, jsonify, request, redirect, url_for, Blueprint
import requests

app = Flask(__name__)
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.cracker
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'Cracker'

bp = Blueprint('place', __name__, url_prefix='/place')

# 맛집 검색하면 키워드에 해당하는 목록을 전달
@bp.route("/search", methods=['GET'])
def get_address():
    place_receive = request.args.get("place_give")
    if (place_receive == ""):
        return ({"result": "success", "msg": "input empty"})
    else:
        searching = place_receive
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
        headers = {
            "Authorization": "KakaoAK b2cd5fe8152984068e62cf5b85fbb75a"
        }
        places = requests.get(url, headers=headers).json()['documents']
        if (places == []):
            return ({"result": "success", "msg": "no result"})
        else:
            return ({"result": "success", "msg": "good", "places": places})


# 선택한 맛집 DB에 저장
@bp.route("/save", methods=['POST'])
def save_place():
    token_receive = request.cookies.get('mytoken')
    try:
        # user 정보
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_mail": payload["id"]})

        # 위치 정보
        place_receive = request.form["place_give"]
        addr_receive = request.form["addr_give"]
        addr_road_receive = request.form["addr_road_give"]
        x_receive = request.form["x_give"]
        y_receive = request.form["y_give"]

        phone_receive = request.form["phone_give"]
        category_receive = request.form["category_give"]

        saved_place = db.matjip.find_one({'matjip_address': addr_receive})

        marker_pic_real = user_info["marker_pic_real"]
        marker_pic = user_info["marker_pic"]

        if (saved_place is None):
            doc = {
                "matjip_name": place_receive,
                "matjip_address": addr_receive,
                "matjip_road_address": addr_road_receive,
                "user_mail": user_info["user_mail"],
                "user_name": user_info["user_name"],
                "x": x_receive,
                "y": y_receive,
                "phone": phone_receive,
                "category":category_receive,
                "marker_pic": marker_pic,
                "marker_pic_real":marker_pic_real
            }
            db.matjip.insert_one(doc)
            return ({"result": "success", "msg": "저장 완료!!"})
        else:
            return ({"result": "success", "msg": "이미 저장 되어있습니다."})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@bp.route("/delete", methods=['DELETE'])
def delete_place():
    token_receive = request.cookies.get('mytoken')
    try:
        # user 정보
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_mail": payload["id"]})

        addr_receive = request.form['addr_give']

        saved_place = db.matjip.find_one({'matjip_address': addr_receive})
        if (user_info["user_mail"] == saved_place["user_mail"]):
            db.matjip.delete_one({'matjip_address': addr_receive})
            return jsonify({'result': 'success', 'msg': '삭제 완료!!'})
        else:
            return jsonify({'result': 'success', 'msg': '계정 정보를 확인하세요.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
