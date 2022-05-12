from pymongo import MongoClient
from flask import Flask, jsonify, Blueprint, request

app = Flask(__name__)
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.cracker
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'Cracker'

bp = Blueprint('map', __name__, url_prefix='/map')

# 맛집 DB에서 값을 가져와서 리스트 출력
@bp.route('/mark', methods=["GET"])
def get_place():
    matjip_list = list(db.matjip.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'matjip_list': matjip_list})