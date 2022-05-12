import boto3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from modules import auth, place, map, blog, user, community
import os

application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})

application.register_blueprint(auth.bp)
application.register_blueprint(place.bp)
application.register_blueprint(map.bp)
application.register_blueprint(blog.bp)
application.register_blueprint(user.bp)
application.register_blueprint(community.bp)

if __name__ == '__main__':
    application.debug = True
    application.run()
