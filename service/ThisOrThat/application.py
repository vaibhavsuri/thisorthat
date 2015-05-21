
import datetime
import json

from flask import Flask
from flask import request
from boto.sqs.message import Message

" importing modules of the current project "
from results import send_my_results, send_others_results
from vote import set_my_decision
from getSQSConn import create_post_queue
from db_table_key_names import Post
from create_post_worker import create_post
# from store_data import *
# import feed
# import vote



app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def hello_world():
    return 'Hello World!'

"""Format (key/value pairs):
uid (Type: integer)
token (Type: integer)
first_name (Type: string)
last_name (Type: string)
"""

@app.route('/user_info',methods=["POST"])
def store_user_info():
    uid = request.form("uid")
    token = request.form("token")
    first_name = request.form("first_name")
    last_name = request.form("last_name")
    store_user_data(uid, token, first_name, last_name)

@app.route('/get_all_tags')
def get_tags():
    return send_tags()

@app.route("/feed/<uid>")
def get_feed(uid):
    return send_feed(uid)

@app.route("/posts/vote/<user_id>/<post_id>/<option_id>")
def place_vote(user_id, post_id, option_id):
    return set_vote(user_id, post_id, option_id)

@app.route("/posts/decision/<user_id>/<post_id>/<option_id>",methods=["POST"])
def place_my_decision(user_id,post_id,option_id):
    set_my_decision(int(user_id),int(post_id),int(option_id))
    return "success"

@app.route("/results/myResults/<user_id>")
def get_my_results(user_id):
    return send_my_results(int(user_id))

@app.route("/results/othersResults/<user_id>")
def get_others_results(user_id):
    return send_others_results(int(user_id))

@app.route("/posts/<user_id>",methods=["POST"])
def insert_post_to_queue(user_id):
    " @todo - return a 200 success message ; add methods = ['POST']"
    my_data = json.loads(request.data)
    post_dict = {Post.get_creator_key():int(user_id)}
    post_dict[Post.get_creation_time_key()] = datetime.datetime.now().strftime('%s')
    reqd_key_mappings = {
                         Post.get_this_img_key():"this_img",
                         Post.get_that_img_key():"that_img",
                         Post.get_this_txt_key():"this_txt",
                         Post.get_that_txt_key():"that_txt",
                         Post.get_tags_key():"tags",
                         Post.get_friends_key():"friends",
                         Post.get_exp_time_key():"exp_time"
                        }
    for _key,mod_key in reqd_key_mappings.iteritems():
        try:
            post_dict[_key] = my_data[mod_key]
        except KeyError,e:
            print mod_key
            print _key
            print e
            return "failure"
    
    #===========================================================================
    # " code that puts a post_dict into a SQS queue"
    # post_dict_message = Message()
    # post_dict_message.set_body(json.dumps(post_dict))
    # create_post_queue.write(post_dict_message)
    #===========================================================================
    create_post(post_dict)
    return "success"
    


@app.errorhandler(500)
def internal_error(error):
    " @todo - log this error "
    return "500 error"

@app.errorhandler(404)
def not_found(error):
    return "404 error"



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001)
