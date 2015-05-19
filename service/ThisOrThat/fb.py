__author__ = 'vaibhavsuri'

import facebook
import getDynamoDB as db
import db_table_key_names as keys
import requests

#returns user's Facebook access token
def get_access_token(user_id):
	user_item = db.get_user_item(user_id)
	return user_item[keys.users_token]

#return the ids of a user's friends
def get_friend_ids(user_id):
	friend_ids = []
	users_token = get_access_token(user_id)
	graph = facebook.GraphAPI(access_token=users_token)
	friends = graph.get_connections("me","friends")
	while(friends['data']):
	    try:
	        for friend in friends['data']:
	            friend_ids.append(friend['id'])
	        friends=requests.get(friends['paging']['next']).json()
	    except KeyError:
	       print "Key Error"
	return friend_ids

#returns the user's email address
def get_email(user_id):
	users_token = get_access_token(user_id)
	graph = facebook.GraphAPI(access_token=users_token)
	info = graph.get_connections("me","")
	if (info.has_key("email")):
		return info["email"]
	else
		return None

#returns the user's email address
def get_email_from_token(user_access_token):
	graph = facebook.GraphAPI(access_token=user_access_token)
	info = graph.get_connections("me","")
	if (info.has_key("email")):
		return info["email"]
	else
		return None

#returns a user's likes (catergory and node_id)
def get_likes(user_id):
	likes_list = []
	users_token = get_access_token(user_id)
	graph = facebook.GraphAPI(access_token=users_token)
	likes = graph.get_connections("me","likes")
	while(likes['data']):
		try:
			for like in likes['data']:
				single_like = {}
				single_like["category"] = like["category"]
				single_like["id"] = like["id"]
				likes_list.append(single_like)
			likes = requests.get(likes['paging']['next']).json()
		except KeyError:
			print "Key Error"
			break
	return likes_list

#returns the ids of books liked by a user
def get_books(user_id):
	books_list = []
	users_token = get_access_token(user_id)
	graph = facebook.GraphAPI(access_token=users_token)
	books = graph.get_connections("me","likes")
	while(books['data']):
		try:
			for book in books['data']:
				books_list.append(book['id'])
			books = requests.get(books['paging']['next']).json()
		except KeyError:
	       print "Key Error"
	return books_list

#returns the ids of music liked by a user
def get_music(user_id):
	music_list = []
	users_token = get_access_token(user_id)
	graph = facebook.GraphAPI(access_token=users_token)
	musics = graph.get_connections("me","likes")
	while(musics['data']):
		try:
			for music in musics['data']:
				music_list.append(music['id'])
			musics = requests.get(musics['paging']['next']).json()
		except KeyError:
	       print "Key Error"
	return music_list

#returns the ids of movies liked by a user
def get_movies(user_id):
	movies_list = []
	users_token = get_access_token(user_id)
	graph = facebook.GraphAPI(access_token=users_token)
	movies = graph.get_connections("me","likes")
	while(movies['data']):
		try:
			for movie in movies['data']:
				movies_list.append(movie['id'])
			movies = requests.get(movies['paging']['next']).json()
		except KeyError:
	       print "Key Error"
	return movies_list