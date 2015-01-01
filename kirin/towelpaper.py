#encoding: utf-8

import json
import time
import datetime
from config import *
from boto.dynamodb.condition import *


sqs = get_sqs()
sns = get_sns()
dynamo = get_dynamo()

user_activate_table = dynamo.get_table(USER_ACTIVATE_TABLE)
user_table = dynamo.get_table(USER_TABLE)

"""
    Polling check if activation code expires and if so delete such code and user
"""

def use_towelpaper():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday_unix_time = yesterday.strftime("%s")
    expired_codes = user_activate_table.scan({
        'Timestamp': LE(yesterday_unix_time)
    })
    expired_count = 0
    for expired_code in expired_codes:
        userid = expired_code['UserID']
        expired_code.delete()
        user = user_table.get_item(userid)
        # Avoid reset password mis-delete
        if user['AccountActive'] != True:
            user.delete()
            expired_count += 1
    print('>>>>>> purge '+str(expired_count)+' expired users >>>>>> run again in 5h :)')


def start_using():
    while(1):
        use_towelpaper()
        time.sleep(5*60*60)



if __name__ == '__main__':
    print('Start using towel paper.')
    start_using()

else:
    print('Fatal Error: Towelpaper is in toilet.')
    exit(0)
