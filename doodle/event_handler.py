#encoding: utf-8

import tornado
import time
import re
from .config import *
from tornado import gen
from .base_handler import *
from .helper import *

class EventHandler(BaseHandler):

	@property 
    def chatgroup_table(self):
        return self.dynamo.get_table(CHATGROUP_TABLE)

    @property 
    def user_topic_table(self):
        return self.dynamo.get_table(USER_TOPIC_TABLE)

    @property 
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

    @property 
    def user_apns_sns_table(self):
        return self.dynamo.get_table(USER_APNS_SNS_TABLE)

    @property 
    def user_inbox_table(self):
        return self.dynamo.get_table(USER_INBOX_TABLE)

    @property
    def user_event_table(self):
    	return self.dynamo.get_table(USER_EVENT_TABLE)

	"""create a new event
	"""
	def post(self):
		pass

	# 