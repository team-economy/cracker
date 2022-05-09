from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.test

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/maps', methods=["GET"])
def get_matjip():
    # 맛집 목록을 Database에서 꺼내오는 API
    # matjip_list = list(db.dddd.find({}, {'_id': False}))
    # likestatus = db.dddd.find_one({"mapy": mapy_receive}, {"like": True, "_id": False})['like']
    # matjip_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)