__author__ = 'vaibhavsuri'

import getDynamoDB as db
import util
import db_table_key_names as keys
#import datetime

#function to check if the post has expired. Returns True if expired, False otherwise.
def verify_time(post_id):
	post_file = db.get_post_item(post_id)
	if (util.get_integer(post_file[keys.post_exp_time]) < util.get_epoch_now()):
		return False
	else:
		return True

#function to verify voting eligibility of the user for a specific post
def verify_not_voted(user_id, post_id):
	user_file = db.get_user_item(user_id)

	#check if user has already voted for this post
	if (user_file[keys.users_voted_posts] is None):
		return True
	elif (post_id in user_file[keys.users_voted_posts]):
		return False

	#check if user is allowed to vote for this post (i.e. if her/him were tagged by the creator of the post)
	if (user_file[keys.users_unvoted_posts] is None):
		return False
	elif (post_id in user_file[keys.users_unvoted_posts]):
		return True
	else:
		return False

#function to apply vote to post database
def update_post_db(user_id, post_id, option_id):
	vote = ""
	post_id_str = str(post_id)

	if (option_id == 1): #if user voted for this
		vote = "this"
		db.conn.update_item("post_db",{keys.post_id:{"N":post_id_str}},{keys.post_this_count:{"Action":"ADD","Value":{"N":"1"}}}) #DB update: increment this_count by 1
	elif (option_id == 2):
		vote = "that"
		db.conn.update_item("post_db",{keys.post_id:{"N":post_id_str}},{keys.post_that_count:{"Action":"ADD","Value":{"N":"1"}}}) #DB update: increment that_count by 1
	elif (option_id == 3):
		vote = "skip"
	post = db.get_post_item(post_id)
	user_pos = util.get_element_position(post[keys.post_frds], keys.post_frds_frd_id, user_id)
	post[keys.post_frds][user_pos][keys.post_frds_vote] = vote
	epoch_time = util.get_epoch_now()
	post[keys.post_frds][user_pos][keys.post_frds_vote_time] = epoch_time
	post[keys.post_frds][user_pos][keys.post_frds_response_time] = epoch_time - post[keys.post_created_time]
	post.partial_save()

#function to apply vote to user database
def update_user_db(user_id, post_id):
	user_item = db.get_user_item(user_id)
	user_item[keys.users_unvoted_posts].remove(post_id)
	if (user_item[keys.users_voted_posts] is None): #if this is the first post the user is voting on
		user_item[keys.users_voted_posts] = [post_id]
	else:
		user_item[keys.users_voted_posts].insert(0, post_id)
	user_item.partial_save()

#function to set a users vote in the database
def set_vote(user_id, post_id, option_id):
	print verify_time(post_id)
	print verify_not_voted(user_id, post_id)
	if (verify_time(post_id) and verify_not_voted(user_id, post_id)): #if post not expired, apply DB updates and return SUCCESS after done
		update_post_db(user_id, post_id, option_id) 
		update_user_db(user_id, post_id)