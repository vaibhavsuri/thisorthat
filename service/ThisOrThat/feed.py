__author__ = 'vaibhavsuri'

import util
import json

###############################
######## GLOBAL VARS #########
TOP_SIZE = 5 #number of top posts to send for feed

###############################

#returns the username (first name + last name) of the creator of a post
def get_username(post_file):
	post_creator_id = post_file["creator"]
	user_file = util.get_user_file(post_creator_id)
	first_name = util.get_string(user_file["first_name"])
	last_name = util.get_string(user_file["last_name"])
	return first_name + " " + last_name

#returns a list containing the top posts for a user's feed
def get_top_posts(post_ids):
	top_posts = []
	top_post_ids = post_ids[1:(TOP_SIZE+1)] #slicing the list based on TOP_SIZE
	for post_id in top_post_ids:
		post_file = util.get_post_file(post_id)
		creator_name = get_username(post_file)
		single_post = {"creator_name": creator_name, "post_id": post_id, "this_img": post_file["this_img"], "that_img": post_file["that_img"], "this_txt": util.get_string(post_file["this_txt"]), "that_txt": util.get_string(post_file["that_txt"])}
		top_posts.append(single_post)
	return top_posts

#returns the feed for a user
def send_feed(uid):
	user_file = util.get_user_file(uid)
	unvoted_post_ids = user_file["unvoted_posts"] #feed only contains posts which are currently not voted on by the user
	top_posts = get_top_posts(unvoted_post_ids)
	feed = {"posts": top_posts}
	feed_json = json.dumps(feed)
	return feed_json



