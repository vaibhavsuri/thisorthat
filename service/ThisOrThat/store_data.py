__author__ = 'ananyapoddar'

import getDynamoDB as db
import db_schema as db_schema
import db_table_key_names as keys
import fb


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
#
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

# Stats

