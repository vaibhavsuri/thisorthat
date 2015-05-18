import datetime
import getMongoDB


#GENERAL UTILITY FUNCTIONS

#returns utf8 encoded string for string values in JSON/BSON
def get_string(input_string):
	return input_string.encode('utf8')

#returns timestamp for now
def get_timestamp_now():
	return datetime.datetime.now()

#returns timestamp for specific date and time parameters
def get_timestamp(year, month, day, hour, mins, secs):
	return datetime.datetime(year, month, day, hour, mins, secs)

#DB SPECIFIC FUNCTIONS

#returns the user file from DB
def get_user_file(uid):
	user_db = getMongoDB.db.user_db
	user_file = user_db.find_one({"id": uid})
	return user_file

#returns the post file from DB
def get_post_file(post_id):
	post_db = getMongoDB.db.post_db
	post_file = post_db.find_one({"id": post_id})
	return post_file

