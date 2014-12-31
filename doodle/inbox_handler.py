#encoding: utf-8

import tornado
import time
from .config import *
from tornado import gen
from .base_handler import *
from helper import *
from boto.dynamodb.condition import *

class InboxHandler(BaseHandler):

    @property 
    def user_inbox_table(self):
        return self.dynamo.get_table(USER_INBOX_TABLE)

    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data
        target_user_id = client_data['target']
        payload = client_data['payload']
        timestamp = str(time.time()).split('.')[0]
        hash_key = md5(payload+timestamp)
        attrs = {
            'MessageID'     : hash_key,
            'UserID'        : target_user_id,
            'JsonMessage'   : payload,
            'Timestamp'     : timestamp
        }
        item = self.table.new_item(
            hash_key=hash_key,
            attrs=attrs
        )
        item.put()

    @async_login_required
    @gen.coroutine
    def get(self):
        response = []
        current_user_id = self.current_user
        messages = self.user_inbox_table.scan({
            'UserID'    :   EQ(current_user_id)
        })
        for message in messages:
            response.append(message)
        self.write_json({'result' : response})










