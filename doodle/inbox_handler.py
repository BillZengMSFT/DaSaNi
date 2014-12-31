#encoding: utf-8

import tornado
import time
from .config import *
from tornado import gen
from .base_handler import *
import boto.dynamodb
import boto.dynamodb.condition

class InboxHandler(BaseHandler):

    @property 
    def inbox_table(self):
        return self.dynamo.get_table(USER_INBOX_TABLE)

    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data
        target_user_id = client_data['target']
        payload = client_data['payload']
        attrs = {
            'UserID'        : target_user_id,
            'JsonMessage'   : payload,
            'Timestamp'     : str(time.time()).split('.')[0]
        }
        item = self.inbox_table.new_item(attrs=attrs)
        item.put()

    @async_login_required
    @gen.coroutine
    def get(self):
        response = []
        inbox_entries = self.inbox_table.query(
            self.current_userid,
            range_key_condition=boto.dynamodb.condition.Condition.LE,
        )
        for entry in inbox_entries:
            response.append(entry)
        self.write_json({'result' : response})










