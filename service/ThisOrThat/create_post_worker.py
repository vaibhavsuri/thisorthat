import json
import threading
import traceback
import time

import requests

from getSQSConn import create_post_queue, stateful_URN, stateful_token, stateful_counter_name
from db_schema import post as post_db_schema
from db_table_key_names import Post, Users
from getDynamoDB import user_db, post_db, get_user_item

pool_size = 2
delay = 5

def thread_job(delay,thread_name):
    global create_post_queue
    while(True):        
        rs=create_post_queue.get_messages(1)
        if (len(rs) > 0):
            if create_post_queue.delete_message(rs[0]):
                _message = rs[0].get_body()
                print _message
                post_query = json.loads(_message)
                create_post(post_query)
        else:
            print "thread:%s ; no messages in queue ; sleeping for %d secs"%(thread_name,delay)
        time.sleep(delay)

def get_latest_post_id():
    payload = {'value':1}
    headers = {'Host': 'www.stateful.co', 'X-Sttc-URN': stateful_URN, 
               'X-Sttc-Token': stateful_token, 'Accept': 'text/plain'}
    increment_url = "http://www.stateful.co/c/%s/inc"%(stateful_counter_name)
    resp = requests.get(increment_url,params=payload,headers=headers)
    if resp.status_code == 200:
        latest_id = int(resp.text)
        return latest_id
    else:
        "todo - handle this else block ; raise an exception ;or log this error"
        pass

def create_post(post_query):
    
    new_post = dict(post_query)
    latest_post_id = new_post[Post.get_id_key()]
    user_id = new_post[Post.get_creator_key()]
    
    " initializing the POST table keys whose data is not received from front-end"
    new_post[Post.get_this_count_key()] = 0
    new_post[Post.get_that_count_key()] = 0
    new_post[Post.get_complete_key()] = False
    new_post[Post.get_decision_key()] = None
    #===========================================================================
    # new_post[Post.get_id_key()] = latest_post_id
    #===========================================================================
    friends_id_li = new_post[Post.get_friends_key()]
    new_post[Post.get_friends_key()] = []
    for index,friend_id in enumerate(friends_id_li):
        li = {}
        li[Post.get_friends_frd_id_key()] = friend_id
        li[Post.get_friends_vote_key()] = None
        li[Post.get_friends_vote_time_key()] = None
        li[Post.get_friends_resp_time_key()] = None
        new_post[Post.get_friends_key()].append(li)

        "adding post-id to unvoted-posts field of users table"
        friend_user_item = get_user_item(friend_id)
        #print friend_user_item
        if (friend_user_item[Users.get_unvoted_posts_key()] is None):
            friend_user_item[Users.get_unvoted_posts_key()] = [latest_post_id]
        else:
            friend_user_item[Users.get_unvoted_posts_key()].append(latest_post_id)
        friend_user_item.partial_save()

    
    " persisting the post-item into post table"
    post_db.put_item(data=new_post)
    
    " adding post-id into created_posts field of users table"
    user_item = get_user_item(user_id)
    if (user_item[Users.get_created_posts_key()] is None):
        user_item[Users.get_created_posts_key()] = [latest_post_id]
    else:
        user_item[Users.get_created_posts_key()].insert(0, latest_post_id)
    user_item.partial_save()
    
def main():
    try:
        threads = []
        for i in range(1, pool_size+1):
            thread_name = "Thread %d"%(i,)
            t = threading.Thread(target=thread_job,name=thread_name,args=(delay,thread_name))
            threads.append(t)
            t.start()
    except:
        print traceback.format_exc()
        print "Unable to start threads"

if __name__ == '__main__':
    main()