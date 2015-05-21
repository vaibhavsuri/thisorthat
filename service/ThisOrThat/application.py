from flask import Flask
from flask import request
import store_data, feed
# import feed
# import vote
# import friends
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

"""Format (key/value pairs):
uid (Type: integer)
token (Type: integer)
first_name (Type: string)
last_name (Type: string)
"""

@app.route('/user_info', methods=["GET", "POST"])
def store_user_info():
    print "VALUE : ",request.data
    uid = request.form("uid")
    token = request.form("token")
    first_name = request.form("first_name")
    last_name = request.form("last_name")
    print "HERE : " + str(uid) +"|" + str(token) +"|"+ str(first_name) + "|" + str(last_name)
    print token
    store_data.store_user_data(uid, token)

@app.route('/get_all_tags')
def store_tags():
    return store_data.send_tags()

@app.route("/feed/<user_id>", methods=["GET"])
def get_feed(user_id):
    return feed.send_feed(user_id)

@app.route("/posts/vote/<user_id>/<post_id>/<option_id>", methods=["POST"])
def place_vote(user_id, post_id, option_id):
    vote.set_vote(user_id, post_id, option_id)

@app.route("/friends/<user_id>/<tag_id>", methods=["GET"])
def get_friends(user_id, tag_id):
    return friends.send_friends(user_id, tag_id)

@app.errorhandler(500)
def internal_error(error):
    return "500 error"

@app.errorhandler(404)
def not_found(error):
    return "404 error"

if __name__ == '__main__':
    app.run("0.0.0.0", port = 8080)
