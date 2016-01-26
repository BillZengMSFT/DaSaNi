import boto.sqs
import boto.sns
import boto.dynamodb
import random

AWS_REGION = 'us-west-2'
AWS_SNS_IOS_APP_ARN = 'arn:aws:sns:us-west-2:878165105740:app/APNS_SANDBOX/CarlorTest'
AWS_ACCESS_KEY_ID = 'AKIAJFBBXT6CLH4UHOLQ'
AWS_ACCESS_KEY = 'h+b1wKAQRjIcu/F4ianavBuGJ5vyENcmNgNYVIZa'

USER_APNS_SNS_TABLE = 'User_APNs_SNS_Table'
USER_TABLE = 'User_Table'
USER_TOPIC_TABLE = 'User_Topic_Table'
USER_ACTIVATE_TABLE = 'User_Activate_Table'
USER_FRIEND_TABLE = 'User_Friend_Table'
USER_INBOX_TABLE = 'User_Inbox_Table'
CHATGROUP_TABLE = 'Chatgroup_Table'
USER_EVENT_TABLE = 'User_Event_Table'
CHAT_RECORD_TABLE = 'Chat_Record_Table'

noosa_names = [
    'honey',
    'blueberry',
    'mango',
    'raspberry',
    'strawberry',
    'peach',
    'passion fruit',
    'lemon',
    'tart cherry',
    'plain',
    'pineapple',
    'coconut',
    'pumpkin'
]

# noosa name
def noosa_name():
    i = random.randint(0, len(noosa_names) - 1)
    return noosa_names[i]

def get_sqs():
    conn = boto.sqs.connect_to_region(
        AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_ACCESS_KEY)
    return conn

def get_sns():
    conn = boto.sns.connect_to_region(
        AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_ACCESS_KEY)
    return conn

def get_dynamo():
    conn = boto.dynamodb.connect_to_region(
        AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_ACCESS_KEY)
    return conn



