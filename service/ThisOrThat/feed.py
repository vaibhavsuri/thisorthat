__author__ = 'vaibhavsuri'

import util
import json
import getDynamoDB as db
import db_table_key_names as keys
import response_format

###############################
######## GLOBAL VARS #########
TOP_SIZE = 5 #number of top posts to send for feed

###############################

#returns a list containing the top posts for a user's feed
def get_top_posts(post_ids):
	top_posts = []
	top_post_ids = post_ids[0:(TOP_SIZE+1)] #slicing the list based on TOP_SIZE
	for post_id in top_post_ids:
		post_file = db.get_post_item(post_id)
		creator_name = db.get_user_name(post_file[keys.post_creator])
		single_post = response_format.get_feed_post(post_id, creator_name, post_file)
		top_posts.append(single_post)	
	return top_posts

#returns the feed for a user
def send_feed(user_id):
	user_item = db.get_user_item(user_id)
	unvoted_post_ids = user_item[keys.users_unvoted_posts] #feed only contains posts which are currently not voted on by the user
	if (unvoted_post_ids is None):
		top_posts = []
	else: 
		top_posts = get_top_posts(unvoted_post_ids)
	feed = {"posts": top_posts}
	feed_json = json.dumps(feed)
	return feed_json

