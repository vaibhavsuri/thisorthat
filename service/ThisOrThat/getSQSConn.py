from boto.sqs.connection import SQSConnection

from getDynamoDB import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

conn = SQSConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
create_post_queue = conn.create_queue('CreatePostQueue')

stateful_URN = "urn:github:5636708"
stateful_token = "C17D-9CBD-C71E-D716"
stateful_counter_name = "post-id-counter"