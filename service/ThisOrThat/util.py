__author__ = 'vaibhavsuri'

import calendar
import time

#GENERAL UTILITY FUNCTIONS

#returns utf8 encoded string for string values in JSON/BSON
def get_string(input_string):
	return input_string.encode('utf8')

#returns timestamp for specific date and time parameters
def get_epoch_now():
	return calendar.timegm(time.gmtime())

def get_element_position(some_list, key, value):
	for i in range(0, len(some_list)):
		if (some_list[i][key] == value):
			return i

#wrapper around int() for converting Decimal(DynamoDB datatype) to integer
def get_integer(val):
	return int(val)
