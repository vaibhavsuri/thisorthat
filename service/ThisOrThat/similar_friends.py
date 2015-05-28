__author__ = 'vaibhavsuri'

import fb
import sec_tags
import getDynamoDB as db
###############################
######## GLOBAL VARS #########
SIMILAR_SIZE = 5 #number of similar friends to store for each tag

###############################

#computing the number of common likes between focus and other user for PRIMARY interests (books, music, movies)
def primary_match_count(listA, listB):
	return len(set(listA).intersection(listB))

#computing the number of common likes between focus and other user for SECONDARY interests
def secondary_match_count(focus_likes, other_likes):
	common_likes = list(set(focus_likes).intersection(other_likes))
	secondary_match = {}
	for like in common_likes:
		this_category = like["category"]
		for tag_key in sec_tags.tags:
			if (this_category in sec_tags.tags[tag_key]):
				if (secondary_match.has_key(tag_key)):
					secondary_match[tag_key] += 1
				else:
					secondary_match[tag_key] = 0
	#padding the dictionary with 0 value keys for the categories not matched at all
	for tag_key in sec_tags.tags:
		if (not secondary_match.has_key(tag_key)):
			secondary_match[tag_key] = 0
	return secondary_match

#storing similar friends in DB
def persist_similar_friends(user_id, friends_likes):
	#the viable similar friends should be at most the number of friends of the user
	viable_similar_size = SIMILAR_SIZE
	if (SIMILAR_SIZE > len(friends_likes)):
		viable_similar_size = len(friends_likes)

	#getting the similar friends item for a user
	similar_friends = db.get_similar_item(user_id)

	#getting top friends for "books"
	sorted_list = sorted(friends_likes, key=lambda k: k["Books"])
	books_friends = [friends_likes[i]["id"] for i in range(0, viable_similar_size)]
	similar_friends["Books"] = books_friends

	#getting top friends for "movies"
	sorted_list = sorted(friends_likes, key=lambda k: k["Movies"])
	movies_friends = [friends_likes[i]["id"] for i in range(0, viable_similar_size)]
	similar_friends["Movies"] = movies_friends

	#getting top friends for "music"
	sorted_list = sorted(friends_likes, key=lambda k: k["Music"])
	music_friends = [friends_likes[i]["id"] for i in range(0, viable_similar_size)]
	similar_friends["Music"] = music_friends

	#getting top friends for secondary tags
	for tag_key in sec_tags.tags:
		sorted_list = sorted(friends_likes, key=lambda k: k[tag_key])
		this_tag_friends = [friends_likes[i]["id"] for i in range(0, viable_similar_size)]
		similar_friends[tag_key] = this_tag_friends

	#partial saving similar friends to DB
	similar_friends.partial_save()

#funtion to compare friends likes with that of the focus user
def compare_friends_likes(user_id):
	#getting the interests of focus user
	focus_user_likes = fb.get_likes(user_id)
	focus_user_books = fb.get_books(user_id)
	focus_user_movies = fb.get_movies(user_id)
	focus_user_music = fb.get_music(user_id)
	#getting friends
	friends_ids = fb.get_friend_ids(user_id)
	friends_likes = []
	for i in friends_ids:
		single_friend = {}
		single_friend["id"] = i
		#getting match counts for primary interests
		single_friend["Books"] = primary_match_count(fb.get_books(i), focus_user_books) 
		single_friend["Movies"] = primary_match_count(fb.get_movies(i), focus_user_movies)
		single_friend["Music"] = primary_match_count(fb.get_music(i), focus_user_music)
		#computing match counts for secondary interests
		single_friend.update(secondary_match_count(focus_user_likes, fb.get_likes(i)))
		friends_likes.append(single_friend)

	persist_similar_friends(user_id, friends_likes) #update in DB

#function to compute similar friends of a user (user_id) and updating in DB
def compute_similar_friends(user_id):
	#the similar friends of the focus user and all her/his friends need to be updated
	users_need_update = fb.get_friend_ids(user_id)
	users_need_update.insert(0, user_id)
	for user in users_need_update: #loop to compute and update the similar friends for each user
		compare_friends_likes(user)
		users_need_update.remove(user)
