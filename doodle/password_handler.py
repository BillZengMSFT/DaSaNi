#encoding: utf-8

import tornado
import json
from tornado import gen
from .base_handler import BaseHandler
from .config import *
from .helper import *

class PasswordHandler(BaseHandler):

	@async_login_required
	@gen.coroutine
	def post():
		pass

	def get(userid, code):
		pass