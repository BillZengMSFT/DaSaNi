#encoding: utf-8

import tornado
import time
from .config import *
from tornado import gen
from .base_handler import *
from .helper import *
from boto.dynamodb2.table import Table

class InboxHandler(BaseHandler):

    @property 
    def user_inbox_table(self):
        return Table('User_Inbox_Table',connection=self.dynamo)

    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data
        target_user_id = client_data['target_user_id']
        payload = client_data['payload']
        timestamp = str(time.time()).split('.')[0]
        hash_key = md5(payload+timestamp)
       
        self.user_inbox_table.put_item(data={
                'MessageID'     : hash_key,
                'UserID'        : target_user_id,
                'JsonMessage'   : payload,
                'Timestamp'     : timestamp
            }
        )
      

    @async_login_required
    @gen.coroutine
    def get(self):
        response = []
        messages = self.user_inbox_table.scan(
            UserID__eq=self.current_userid
        )
        for message in messages:
            response.append(message)
        self.write_json({'result' : response})










