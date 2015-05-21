__author__ = 'ananyapoddar'

import getDynamoDB as db
import db_schema as db_schema
import db_table_key_names as keys
import fb
from collections import OrderedDict


# Global Cache #
tags_cache = {}


def store_user_data(uid, token):
    """ Stores user_info into the 'user' DB Schema created in db_schema
    Get Email, first name, last name by function calls"""

    # access token = "CAACEdEose0cBAEZBAbuXNqZBx6iC6snMwYscB3mZC9cDADpGOJSgPVoXWu28bUcRJJzsSgIJFsFIOouuj6g9xHZCxojeelKNZBRKRsHKM76ap4Yr9ZA1CT0qyXANRONtBfUp5Xf3ByzfAZBZA9RZB6LWciIO5J0VLMdvly6DFBurWdTArD5lLPYYZAb5hcgiznOG7hSOXNIGUNlDrfyZBNZB246ZBWMxCVnQQhXqzT3AZC3kpV0AZDZD"
    # user_id = "ananya0112@gmail.com"
    db_schema.user[keys.users_id] = uid
    db_schema.user[keys.users_token] = token

    # if token.length>0:
    email_id = fb.get_email_from_token(token)
    if not email_id: # If email_id is None
        email_id = ""
    db_schema.user[keys.users_email] = email_id

    # Get firstname, lastname| validate | Pending #
    # db.user_db.put_item(data = db_schema.user)
    print db_schema.user

# # Next : Tags (Verify)
# def cache_tags():
#     tags_db = db.tags_db
#     # get all tags from the db #
#     all_tags = tags_db.find()
#     tags_cache = [each_tag.to_mongo() for each_tag in all_tags]
#     return tags_cache
#
# tags_cache = cache_tags()
#
# def send_tags():
#     return tags_cache


def create_frds_dict(user_id):
    user_friends = {}
    # The friends who have ever posted in response to this user_id | My aggregate dictionary
    user_item = db.get_user_item(user_id)
    all_post_id = user_item[keys.users_created_posts]
    users_posts_count = len(all_post_id)
    for post_id in all_post_id:
        post = db.get_post_item(post_id)
        # A SINGLE post item with all the info extracted from the database :
        post_friends, post_decision = post[keys.post_frds], post[keys.post_decision]
        for friend in post_friends:
            # A single friend item/object!
            friend_id, response_time = friend[keys.post_frds_frd_id], friend[keys.post_frds_response_time]
            voted_count, intersection_count = 0, 0
            if friend[keys.post_frds_vote].strip() != "skip":
                voted_count = 1
            # Count the intersection votes :
            if friend[keys.post_frds_vote].strip() == post_decision.strip():
                intersection_count = 1
            if friend_id in user_friends:
                # Simply update values
                user_friends[friend_id]["tag_count"] += 1
                user_friends[friend_id]["voted_count"] += voted_count
                user_friends[friend_id]["total_response_time"] += response_time
                user_friends[friend_id]["match_votes"] += intersection_count

            elif friend_id not in user_friends:
                # If this friend appears for the first time in the list, put initial values i.e value of this object
                friend_val = {"tag_count": 1, "voted_count": voted_count, "total_response_time": response_time,
                              "match_votes": intersection_count}
                user_friends[friend_id] = friend_val
    return user_friends


def get_fastest_responders(user_friends, max_no):
    # Send user_friends dictionary for that corresponding user_id | sorted(a.items(), key=lambda x:x[1][1])
    # Returns a list of user_id's | max_no represents the total no. of user_id's that will be returned
    fast_resp = OrderedDict(sorted(user_friends.items(), key=lambda kv: kv[1]['total_response_time']/kv[1]['voted_count']))
    if len(fast_resp) < max_no:
        max_no = len(fast_resp)
    i = 0
    fastest_resp = []
    while i < max_no:
        score = fast_resp[fast_resp.keys()[i]]['total_response_time']/fast_resp[fast_resp.keys()[i]]['voted_count']
        fastest_resp.append((fast_resp.keys()[i], score))
        i += 1
    return fastest_resp


def get_frequent_responders(user_friends, max_no):
    # Send user_friends dictionary for that corresponding user_id | sorted(a.items(), key=lambda x:x[1][1])
    # max_no represents the total no. of user_id's that will be returned
    freq_resp = OrderedDict(sorted(user_friends.items(), key=lambda kv: kv[1]['voted_count']/kv[1]['tag_count'], reverse=True))
    if len(freq_resp) < max_no:
        max_no = len(freq_resp)
    i = 0
    frequent_resp = []
    while i < max_no:
        score = freq_resp[freq_resp.keys()[i]]['voted_count']/freq_resp[freq_resp.keys()[i]]['tag_count']
        frequent_resp.append((freq_resp.keys()[i], score))
        i += 1
    return frequent_resp


def get_top_influencer(user_friends, max_no):
    # max_no represents the total no. of user_id's that will be returned
    top_inf = OrderedDict(sorted(user_friends.items(), key=lambda kv: kv[1]['match_votes']/kv[1]['tag_count'], reverse=True))
    if len(top_inf) < max_no:
        max_no = len(top_inf)
    i = 0
    top_influencer = []
    while i < max_no:
        score = top_inf[top_inf.keys()[i]]['match_votes']/top_inf[top_inf.keys()[i]]['tag_count']
        top_influencer.append((top_inf.keys()[i], score))
        i += 1
    return top_influencer

def get_stat_attr(list_user_data):
    """ Given a list of <max_no> (user_id, scores), will create <max_no> size list of objects containing attributes
    firstname, lastname, profile_photo, score | fb.get_user_details(user_id) returns an object (fn, ln, pp)"""
    list_user_obj = []
    for user_data in list_user_data:
        user_obj = fb.get_user_details(user_data[0])
        user_obj["score"] = user_data[1]
        list_user_obj.append(user_obj)
    return list_user_obj


def get_statistics(user_id, max_no):
    user_friends = create_frds_dict(user_id)
    # The next 3 functions returns a list of (user_id, score)
    fastest_responders = get_fastest_responders(user_friends, max_no)
    frequent_responder = get_frequent_responders(user_friends, max_no)
    top_influencers = get_top_influencer(user_friends, max_no)
    statistics = {"fastest_responders": get_stat_attr(fastest_responders), "frequent_responder":
                                get_stat_attr(frequent_responder), "top_influencers": get_stat_attr(top_influencers)}
    return statistics

