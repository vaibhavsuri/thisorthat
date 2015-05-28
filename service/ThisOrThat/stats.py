__author__ = 'ananyapoddar'

import json
import getDynamoDB as db
import similar_friends, fb
import db_table_key_names as keys
from bar_plot import bar_plot
import getS3

from collections import OrderedDict


def create_frds_dict(user_id):
    user_friends = {}
    # The friends who have ever posted in response to this user_id | My aggregate dictionary
    user_item = db.get_user_item(user_id)
    all_post_id = user_item[keys.users_created_posts]
    # users_posts_count = len(all_post_id)
    for post_id in all_post_id:
        post = db.get_post_item(post_id)
        # A SINGLE post item with all the info extracted from the database :
        post_friends, post_decision = post[keys.post_frds], post[keys.post_decision]
        for friend in post_friends:
            # A single friend item/object!
            friend_id, response_time = friend[keys.post_frds_frd_id], friend[keys.post_frds_response_time]
            voted_count, intersection_count = 0, 0
            if friend[keys.post_frds_vote]:
                # Perform these steps if & only if the friend vote is not None
                if friend[keys.post_frds_vote].strip() != "skip":
                    voted_count = 1
                # Count the intersection votes :
                if post_decision:
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
    print "User-Friends aggregate dictionary : ", user_friends
    return user_friends


def get_fastest_responders(user_friends, max_no):
    # Send user_friends dictionary for that corresponding user_id | sorted(a.items(), key=lambda x:x[1][1])
    # Returns a list of user_id's | max_no represents the total no. of user_id's that will be returned
    print "Starting fastest responders"
    fast_resp = OrderedDict(sorted(user_friends.items(), key=lambda kv: kv[1]['total_response_time']/kv[1]['voted_count']))
    if len(fast_resp) < max_no:
        max_no = len(fast_resp)
    i = 0
    fastest_resp = []
    while i < max_no:
        score = fast_resp[fast_resp.keys()[i]]['total_response_time']/fast_resp[fast_resp.keys()[i]]['voted_count']
        fastest_resp.append((fast_resp.keys()[i], score))
        i += 1
    print "Fastest resp : ", fastest_resp
    return fastest_resp


def get_frequent_responders(user_friends, max_no):
    # Send user_friends dictionary for that corresponding user_id | sorted(a.items(), key=lambda x:x[1][1])
    # max_no represents the total no. of user_id's that will be returned
    print "Starting frequent responders"
    freq_resp = OrderedDict(sorted(user_friends.items(), key=lambda kv: kv[1]['voted_count']/kv[1]['tag_count'], reverse=True))
    if len(freq_resp) < max_no:
        max_no = len(freq_resp)
    i = 0
    frequent_resp = []
    while i < max_no:
        score = freq_resp[freq_resp.keys()[i]]['voted_count']/freq_resp[freq_resp.keys()[i]]['tag_count']
        frequent_resp.append((freq_resp.keys()[i], score))
        i += 1
    print "Freq resp ", frequent_resp
    return frequent_resp


def get_top_influencer(user_friends, max_no):
    # max_no represents the total no. of user_id's that will be returned
    print "Starting Top Influencer "
    top_inf = OrderedDict(sorted(user_friends.items(), key=lambda kv: kv[1]['match_votes']/kv[1]['tag_count'], reverse=True))
    if len(top_inf) < max_no:
        max_no = len(top_inf)
    i = 0
    top_influencer = []
    while i < max_no:
        score = top_inf[top_inf.keys()[i]]['match_votes']/top_inf[top_inf.keys()[i]]['tag_count']
        top_influencer.append((top_inf.keys()[i], score))
        i += 1
    print "Top INF", top_influencer
    return top_influencer

def get_stat_attr(list_user_data,user_id,type="1"):
    """ Given a list of <max_no> (user_id, scores), will create <max_no> size list of objects containing attributes
    firstname, lastname, profile_photo, score | fb.get_user_details(user_id) returns an object (fn, ln, pp)"""

    #===========================================================================
    # list_user_obj = []
    # for user_data in list_user_data:
    #     user_obj = fb.get_user_details(user_data[0])
    #     user_obj["score"] = user_data[1]
    #     list_user_obj.append(user_obj)
    # 
    #===========================================================================
    
    x_axis_vals = []
    y_axis_vals = []
    for user_data in list_user_data:
        user_obj = fb.get_user_details(user_data[0])
        x_axis_vals.append(user_obj["first_name"].split()[0])
        y_axis_vals.append(user_data[1])
    
    if type == "1":
        fig_name = "%d_fastest_responders.jpg"%(user_id)
        y_label = "Avg. Response Time"
        bar_title = " Fastest Responders "
    elif type == "2":
        fig_name = "%d_frequent_responders.jpg"%(user_id)
        y_label = "Number of Times Voted "
        bar_title = " Frequent Responders "
    elif type == "3":
        fig_name = "%d_Top_Influencers.jpg"%(user_id)
        y_label = "Percentage Match "
        bar_title = " Top Influencers "
    
    " creating the bar plot"
    bar_plot(x_axis_vals,y_axis_vals,fig_name=fig_name,y_label=y_label,bar_title=bar_title)
    
    " storing in S3"
    file_p = open(fig_name,'rb')
    getS3.store_file(fig_name.split(".")[0], file_p)
    
    curr_url = "https://s3-us-west-2.amazonaws.com/this-or-that-image-bucket/%s"%(fig_name)
    return curr_url


def get_statistics(user_id, max_no):
    user_friends = create_frds_dict(user_id)
    # The next 3 functions returns a list of (user_id, score)
    fastest_responders = get_fastest_responders(user_friends, max_no)
    frequent_responder = get_frequent_responders(user_friends, max_no)
    top_influencers = get_top_influencer(user_friends, max_no)
    statistics = {
                  "fastest_responders": get_stat_attr(fastest_responders,user_id,"1"), 
                  "frequent_responders": get_stat_attr(frequent_responder,user_id,"2"),
                  "top_influencers": get_stat_attr(top_influencers,user_id,"3")
                  }
    print statistics
    return json.dumps(statistics)

if __name__ == '__main__':
    get_statistics(1428248470828832, 5)