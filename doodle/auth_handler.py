#encoding: utf-8

import tornado
from .config import *
from tornado import gen
from .base_handler import *

class AuthHandler(BaseHandler):

    @property 
    def table(self):
        return self.dynamo.get_table(USER_TOPIC_TABLE)

"""
    User Login
"""
    
    @gen.coroutine
    def post(self):
        