
"Post table keys"
post_id = "id"
post_creator = "creator"
post_this_img = "thisImage"
post_that_img = "thatImage"
post_this_txt = "thisText"
post_that_txt = "thatText"
post_tags = "tags"
post_frds = "friends"
post_frds_frd_id = "friendId"
post_frds_vote = "vote"
post_frds_vote_time = "voteTime"
post_frds_response_time = "responseTime"
post_created_time = "creationTime"
post_exp_time = "expirationTime"
post_this_count = "thisCount"
post_that_count = "thatCount"
post_is_complete = "isComplete"
post_decision = "decision"

"Users table keys"
users_id = "id"
users_fname = "firstName"
users_lname = "lastName"
users_email = "email"
users_token = "facebookToken"
users_last_seen = "lastSeenTimeStamp"
users_location = "location"
users_location_lat = "lat"
users_location_long = "long"
users_location_place = "place"
users_created_posts = "createdPosts"
users_voted_posts = "votedPosts"
users_unvoted_posts = "unvotedPosts"

"Tag table keys"
tag_id = "id"
tag_name = "name"

class Post:
    
    @staticmethod
    def get_id_key():
        return post_id

    @staticmethod
    def get_creator_key():
        return post_creator
    
    @staticmethod
    def get_this_img_key():
        return post_this_img
    
    @staticmethod
    def get_that_img_key():
        return post_that_img
    
    @staticmethod
    def get_this_txt_key():
        return post_this_txt

    @staticmethod
    def get_that_txt_key():
        return post_that_txt
    
    @staticmethod
    def get_tags_key():
        return post_tags
    
    @staticmethod
    def get_friends_key():
        return post_frds
    
    @staticmethod
    def get_friends_frd_id_key():
        return post_frds_frd_id
    
    @staticmethod
    def get_friends_vote_key():
        return posts_frds_vote
    
    @staticmethod
    def get_friends_vote_time_key():
        return post_frds_vote_time
    
    @staticmethod
    def get_friends_resp_time_key():
        return post_frds_response_time
    
    @staticmethod
    def get_creation_time_key():
        return post_created_time
    
    @staticmethod
    def get_exp_time_key():
        return post_exp_time
    
    @staticmethod
    def get_this_count_key():
        return post_this_count
    
    @staticmethod
    def get_that_count_key():
        return post_that_count
    
    @staticmethod
    def get_complete_key():
        return post_is_complete
    
    @staticmethod
    def get_decision_key():
        return post_decision
    

class Users:
    
    @staticmethod
    def get_id_key():
        return users_id
    
    @staticmethod
    def get_fname_key():
        return users_fname
    
    @staticmethod
    def get_lname_key():
        return users_lname
    
    @staticmethod
    def get_email_key():
        return users_email
    
    @staticmethod
    def get_token_key():
        return users_token
    
    @staticmethod
    def get_location_key():
        return users_location
    
    @staticmethod
    def get_created_posts_key():
        return users_created_posts
    
    @staticmethod
    def get_voted_posts_key():
        return users_voted_posts
    
    @staticmethod
    def get_unvoted_posts_key():
        return users_unvoted_posts
    
class Tags:
    
    @staticmethod
    def get_id_key():
        return tag_id

    @staticmethod
    def get_name_key():
        return tag_name

if __name__ == '__main__':
    print Post.get_id_key()
    print Users.get_email_key()
    print Tags.get_name_key()