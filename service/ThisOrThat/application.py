from flask import Flask
from flask import request
import store_data, feed, vote, friends

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user_info')
def store_user_info():
    print "VALUE : ",request.form
    uid = request.form("uid")
    token = request.form("token")
    first_name = request.form("first_name")
    last_name = request.form("last_name")
    store_data.store_user_data(uid, token, first_name, last_name)


@app.route('/get_all_tags')
def store_tags():
    return store_data.send_tags()


@app.route("/feed/<user_id>", methods=["GET"])
def get_feed(user_id):
    return feed.send_feed(int(user_id))


@app.route("/get_statistics/<user_id>/<max_no>", methods=["GET"])
def get_statistics(user_id, max_no):
    return store_data.get_statistics(int(user_id), int(max_no))


@app.route("/posts/vote/<user_id>/<post_id>/<option_id>", methods=["POST"])
def place_vote(user_id, post_id, option_id):
    return vote.set_vote(int(user_id), int(post_id), int(option_id))


@app.route("/friends/<user_id>/<tag_id>", methods=["GET"])
def get_friends(user_id, tag_id):
    return friends.send_friends(int(user_id), int(tag_id))


############## TESTING SECTION #####################

# ####  COMPUTING SIMILAR FRIENDS ####
# @app.route("/similar/<user_id>/", methods=["GET"])
# def set_similar_friends(user_id):
#     similar_friends.compute_similar_friends(int(user_id))
#     return "SIMILAR FRIENDS SET"

####################################################

@app.errorhandler(500)
def internal_error(error):
    return "500 error"

@app.errorhandler(404)
def not_found(error):
    return "404 error"

if __name__ == '__main__':
    app.run("0.0.0.0", port = 8080, debug=True)
