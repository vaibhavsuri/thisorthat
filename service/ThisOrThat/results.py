__author__ = "sreeram"

import json

def send_my_results(user_id):
    """ returns the my-results of a user_id """
    my_results = []
    " get all post-ids of the posts created by this user_id"
    created_post_ids = get_all_created_post_ids(user_id)
    
    " iterate over each post and store its details"
    for _post_id in created_post_ids:
        my_results.append(get_post_details(_post_id))

    " converting to json format"
    my_results_json = json.dumps(my_results)
    return my_results_json

def send_others_results(user_id):
    """ returns the other-post-results of a user_id """
    other_results = []
    " get all post-ids of the posts voted by this user_id"
    voted_post_ids = get_all_voted_post_ids(user_id)
    
    " iterate over each post and store its details"
    for _post_id in voted_post_ids:
        other_results.append(get_post_details(_post_id))

    " converting to json format"
    other_results_json = json.dumps(other_results)
    return other_results_json


if __name__ == "__main__":
    send_my_results(1)