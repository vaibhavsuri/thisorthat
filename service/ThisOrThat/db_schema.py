__author__ = 'vaibhavsuri'

import db_table_key_names as keys
import sec_tags

post = {keys.post_id: 0,
		keys.post_creator: 0,
		keys.post_this_img: 0,
		keys.post_that_img: 0,
		keys.post_this_txt: "",
		keys.post_that_txt: "",
		keys.post_tags: [],
		keys.post_frds: [],
		keys.post_created_time: 0.0,
		keys.post_exp_time: 0.0,
		keys.post_this_count: 0,
		keys.post_that_count: 0,
		keys.post_is_complete: False,
		keys.post_decision: None
}

user = {keys.users_id: 0,
		keys.users_fname: "",
		keys.users_lname: "",
		keys.users_email: "",
		keys.users_token: "",
		keys.users_last_seen: "",
		keys.users_location:{keys.users_location_lat:0.0, keys.users_location_long:0.0, keys.users_location_place:""},
		keys.users_created_posts: [],
		keys.users_voted_posts: [],
		keys.users_unvoted_posts: []
}

tag = {keys.tag_id : 0, keys.tag_name : ""}

def get_similar_template():
	similar = {keys.users_id: 0,
			   keys.similar_books: [],
			   keys.similar_movies: [],
			   keys.similar_music: [],
	}
	for tag in sec_tags.tags:
		similar[tag] = []
	return similar

def validate(item, item_type):
    if item_type == "post":
        auth_item = post
    elif item_type == "user":
        auth_item = user
    else:
        auth_item = tag
    try:
        for key in auth_item:
            if (type(auth_item[key]) != type(item[key])):
                return False
        return True
    except Exception, e:
        print e