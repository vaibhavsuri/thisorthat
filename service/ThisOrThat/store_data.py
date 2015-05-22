__author__ = 'ananyapoddar'

import getDynamoDB as db
import db_schema as db_schema
import db_table_key_names as keys
import fb

def store_user_data(uid, token, first_name, last_name):
    """ Stores user_info into the 'user' DB Schema created in db_schema
    Get Email, first name, last name by function calls"""
    ##
    db_schema.user[keys.users_id] = uid
    db_schema.user[keys.users_token] = token
    db_schema.user[keys.users_fname] = first_name
    db_schema.user[keys.users_lname] = last_name

    email_id = fb.get_email_from_token(token)
    db_schema.user[keys.users_email] = email_id
    # Get firstname, lastname Pending #
    user_inserted = db.user_db.put_item(data = db_schema.user)

    similar_item = db_schema.get_similar_template()
    similar_item[keys.users_id] = uid
    sim_item_inserted = db.similar_db.put_item(data=similar_item)
    similar_friends.compute_similar_friends(uid)