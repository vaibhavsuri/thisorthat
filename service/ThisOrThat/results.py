__author__ = "sreeram"

import json

" project specific imports "
import db_table_key_names as db_keys
from getDynamoDB import get_user_item, get_post_item

def get_all_created_post_ids(user_id):
    user_item = get_user_item(user_id)
    created_post_ids = user_item.get(db_keys.Users.get_created_posts_key())
    return created_post_ids

def get_all_voted_post_ids(user_id):
    user_item = get_user_item(user_id)
    voted_post_ids = user_item.get(db_keys.Users.get_voted_posts_key())
    return voted_post_ids

def get_post_details_my_results(post_id):
    post_item = get_post_item(post_id)
    _post_details = {}
    _post_details["post_id"] = int(post_item.get(db_keys.Post.get_id_key()))
    _post_details["this_img"] = post_item.get(db_keys.Post.get_this_img_key())
    _post_details["that_img"] = post_item.get(db_keys.Post.get_that_img_key())
    _post_details["this_txt"] = post_item.get(db_keys.Post.get_this_txt_key())
    _post_details["that_txt"] = post_item.get(db_keys.Post.get_that_txt_key())
    _post_details["this_count"] = int(post_item.get(db_keys.Post.get_this_count_key()))
    _post_details["that_count"] = int(post_item.get(db_keys.Post.get_that_count_key()))
    if post_item.get(db_keys.Post.get_decision_key()) is None:
        _post_details["has_decided"] = False
    else:
        _post_details["has_decided"] = True
    return _post_details
    
def get_post_details_others_results(post_id):
    post_item = get_post_item(post_id)
    user_id = post_item.get(db_keys.Post.get_creator_key())
    user_item = get_user_item(user_id)
    _post_details = {}
    _post_details["post_id"] = int(post_item.get(db_keys.Post.get_id_key()))
    _post_details["creator_first_name"] = user_item.get(db_keys.Users.get_fname_key())
    _post_details["creator_last_name"] = user_item.get(db_keys.Users.get_lname_key())
    _post_details["this_img"] = post_item.get(db_keys.Post.get_this_img_key())
    _post_details["that_img"] = post_item.get(db_keys.Post.get_that_img_key())
    _post_details["this_txt"] = post_item.get(db_keys.Post.get_this_txt_key())
    _post_details["that_txt"] = post_item.get(db_keys.Post.get_that_txt_key())
    _post_details["this_count"] = int(post_item.get(db_keys.Post.get_this_count_key()))
    _post_details["that_count"] = int(post_item.get(db_keys.Post.get_that_count_key()))
    return _post_details


def send_my_results(user_id):
    """ returns the my-results of a user_id """
    my_results = []
    
    " get all post-ids of the posts created by this user_id"
    created_post_ids = get_all_created_post_ids(user_id)
    
    " iterate over each post and store its details"
    for _post_id in created_post_ids:
        my_results.append(get_post_details_my_results(_post_id))

    return json.dumps(my_results)

def send_others_results(user_id):
    """ returns the other-post-results of a user_id """
    other_results = []
    
    " get all post-ids of the posts voted by this user_id"
    voted_post_ids = get_all_voted_post_ids(user_id)
    
    " iterate over each post and store its details"
    if voted_post_ids is None:
        pass
    else:
        for _post_id in voted_post_ids:
            other_results.append(get_post_details_others_results(_post_id))

    return json.dumps(other_results)

if __name__ == "__main__":
    send_my_results(1)