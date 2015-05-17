__author__ = 'ananyapoddar'

import getMongoDB


# Global Cache #
tags_cache = {}

def store_user_data(uid, token, first_name, last_name):
    user_info = {"uid": uid,
                 "token": token,
                 "first_name": first_name,
                 "last_name": last_name
                }

    # user_db = getMongoDB.db.user_db
    # post_id = user_db.insert_one(user_info).inserted_id
    # print post_id

# Next : Tags (Verify)
def cache_tags():
    tags_db = getMongoDB.db.tags_db
    # get all tags from the db #
    all_tags = tags_db.find()
    tags_cache = [each_tag.to_mongo() for each_tag in all_tags]
    return tags_cache

tags_cache = cache_tags()

def send_tags():
    return tags_cache

# Stats

