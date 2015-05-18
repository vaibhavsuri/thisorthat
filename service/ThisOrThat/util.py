import datetime
import calendar

#GENERAL UTILITY FUNCTIONS

#returns utf8 encoded string for string values in JSON/BSON
def get_string(input_string):
	return input_string.encode('utf8')

#returns timestamp for specific date and time parameters
def get_epoch_now():
	return calendar.timegm(time.gmtime())


