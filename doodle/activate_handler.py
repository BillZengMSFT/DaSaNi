import tornado
import json
from tornado import gen
from .base_handler import BaseHandler
from config import *



class ActivateHandler(BaseHandler):
	@property
    def table(self):
        return self.dynamo.get_table(User_Table)

	@property
    def activate_table(self):
        return self.dynamo.get_table(Activate_Table)

	@gen.coroutine
	def post(self):
		"""
			PAYLOAD:
			{
				userid: USERID
				code : ACTIVATECODE ## EX: "5DE3C"
			}
		"""
		code = self.data["code"]
		userid = self.data["userid"]
		code_is_real =  self.activate_table.has_item(userid)
		if code_is_real:
			activator = self.activate_table.get_item(userid)
			if activator["code"] == code:
				user_data = self.table.get_item(userid)
				user_data[""]



