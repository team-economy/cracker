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
        place_title = db.matjip.find_one({"matjip_name":place}, {"_id": False})
        user_info = db.users.find_one({"user_mail":payload['id']}, {"_id": False})

        print(place_title)

        return render_template('community.html', user_info=user_info, place_title=place_title)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))