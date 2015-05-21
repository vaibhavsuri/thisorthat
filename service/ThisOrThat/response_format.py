__author__ = 'vaibhavsuri'

import db_table_key_names as keys
import util

feed_post = {"creator_name": "",
			"post_id": 0,
			"this_img": 0,
			"that_img": 0,
			"this_txt": 0,
			"that_txt": 0
}

#returns a single feed post filled with required information
def get_feed_post(post_id, creator_name, post_file):
	new_feed_post = dict(feed_post)
	new_feed_post["creator_name"] = creator_name
	new_feed_post["post_id"] = util.get_integer(post_id)
	new_feed_post["this_img"] = post_file[keys.post_this_img]
	new_feed_post["that_img"] = post_file[keys.post_that_img]
	new_feed_post["this_txt"] = post_file[keys.post_this_txt]
	new_feed_post["that_txt"] = post_file[keys.post_that_txt]
	return new_feed_post


segmented_friends = {"suggested": [],
					"others": []	
}

#returns the friends for a post following the required segmentation
def get_segmented_friends(suggested_list, others_list):
	new_segmented_friends = dict(segmented_friends)
	new_segmented_friends["suggested"] = suggested_list
	new_segmented_friends["others"] = others_list
	return new_segmented_friends 