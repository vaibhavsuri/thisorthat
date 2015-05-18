__author__ = 'vaibhavsuri'

import getMongoDB
import util
#import datetime

#function to check if the post has expired. Returns True if expired, False otherwise.
def verify_time(post_id):
	post_file = post_db.find_one({"id": post_id})
	if (post_file["exp_time"] < datetime.datetime.now()):
		return False
	else:
		return True

#function to apply vote to post database
def update_post_db(user_id, post_id, option_id):
	post_db = getMongoDB.db.post_db
	vote = ""
	if (option_id == 1): #if user voted for this
		vote = "this"
		post_db.update({ "id": post_id }, { "$inc":{"this_count": 1}}) #DB update: increment this_count by 1
	elif (option_id == 2):
		vote = "that"
		post_db.update({ "id": post_id }, { "$inc":{"that_count": 1}}) #DB update: increment that_count by 1
	post_db.update({ "id": post_id, "friends.friend_id": user_id }, { "$set":{"friends.$.vote": vote}}) #DB update: setting vote value for user
	post_db.update({ "id": post_id, "friends.friend_id": user_id }, { "$set":{"friends.$.vote_time": util.get_timestamp_now()}}) #DB update: setting vote time for user

#function to apply vote to user database
def update_user_db(user_id, post_id):
	user_db = getMongoDB.db.user_db
	user_db.update({ "id": user_id, "unvoted_posts": post_id }, { "$unset":{"unvoted_posts.$": ""}}) #DB update: removing post_id from unvoted_posts
	user_db.update( { "id": user_id }, { "$push":{"voted_posts": {"$each": [post_id], "$position": 0 } } }) #DB update: prepending post_id to voted posts

#function to set a users vote in the database
def set_vote(user_id, post_id, option_id):
	if (verify_time(post_id)): #if post not expired, apply DB updates and return SUCCESS after done
		update_post_db(user_id, post_id, option_id) 
		update_user_db(user_id, post_id)
		return "SUCCESS"
	else: #else post expired, and we return FAILURE 
		return "FAILURE"