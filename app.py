from flask import Flask

from controllers import auth, place, map, blog, user, community

app = Flask(__name__)

app.register_blueprint(auth.bp)
app.register_blueprint(place.bp)
app.register_blueprint(map.bp)
app.register_blueprint(blog.bp)
app.register_blueprint(user.bp)
app.register_blueprint(community.bp)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
