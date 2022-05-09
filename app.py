from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.cracker

@app.route('/')
def main():
    return render_template("index.html")

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
    doc = {
        "matjip_name":place_receive,
        "matjip_address":addr_receive,
        "matjip_road_address":addr_road_receive,
        "user_name":'cheoljin',
        "profile_name":'cheoljin'
    }
    db.matjip.insert_one(doc)
    return({"result":"success"})

# 맛집 DB에서 값을 가져와서 리스트 출력
@app.route('/get_place', methods=["GET"])
def get_place():

    matjip_list = list(db.matjip.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/maps', methods=["GET"])
def get_matjip():

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)