#encoding: utf-8

import tornado
import time
from .config import *
from tornado import gen
from .base_handler import *
from boto.dynamodb.condition.Condition import *

class InboxHandler(BaseHandler):

    @property 
    def table(self):
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
        item = self.table.new_item(
            hash_key=UserID,
            attrs=attrs
        )
        item.put()

    @async_login_required
    @gen.coroutine
    def get(self):
        response = []
        current_user_id = self.current_user
        inbox_entries = self.table.query(
            current_user_id,
            range_key_condition=LE,
        )
        for entry in inbox_entries:
            response.append(entry)
        self.write_json({'result' : response})










