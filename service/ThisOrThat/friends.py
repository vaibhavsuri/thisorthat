import fb
import json
import getDynamoDb as db
import db_table_key_names as keys
import response_format 

#returns the ids of similar friends for a tag
def get_friend_ids_tag(user_id, tag_name):
	similar_item = db.get_similar_item(user_id)
	friend_ids = []
	for friend in similar_item[tag_name]:
		friend_ids.append(int(friend))
	return friend_ids

#returns the friends of a user segmented based on "suggested" and others
def segment_friends(user_id, tag_name):
	all_friends = fb.get_friend_ids(user_id)
	similar_friend_ids = get_friend_ids_tag(user_id, tag_name)
	other_friend_ids = list(set(all_friends) - set(similar_friend_ids))
	#constructing list of suggested friends (id and name)
	suggested = []
	for friend_id in similar_friend_ids:
		one_friend = {}
		one_friend["friend_id"] = friend_id
		one_friend["friend_name"] = db.get_user_name(friend_id)
		suggested.append(one_friend)
	#constructing list of other friends (id and name)
	others = []
	for friend_id in other_friend_ids:
		one_friend = {}
		one_friend["friend_id"] = friend_id
		one_friend["friend_name"] = db.get_user_name(friend_id)
		others.append(one_friend)
	#formatting the information
	segmented_friends = response_format.get_segmented_friends(suggested, others)
	return segmented_friends

#returns the taggable friends for a post
def send_friends(user_id, tag_id):
	tag_name = db.get_tag_name(tag_id)
	segmented_friends = segment_friends(user_id, tag_name)
	segmented_friends_json = json.dumps(segmented_friends) #creating JSON
	return segmented_friends_json

