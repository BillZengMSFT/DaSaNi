#encoding: utf-8

import tornado
import json
from tornado import gen
from dynamo import User
from functools import wraps

class BaseHandler(tornado.web.RequestHandler):

    @property
    def sqs(self):
        return self.settings['sqs']

    @property 
    def sns(self):
        return self.settings['sns']

    @property 
    def dynamo(self):
        return self.settings['dynamo']

    @property
    def memcache(self):
        return self.settings['memcache']

    @property
    def data(self):
        return json.loads(self.request.body.decode('utf-8'))

    """ TODO For Every Handler
        filter out every input dictionary
    """

    def input_firewall(input_dict):
        pass

    """ TODO For Every Handler
        filter out every output dictionary
    """

    def output_firewall(input_dict):
        pass

    """ User token authorization
            user here is user id
    """

    @gen.coroutine
    def authorize_user(self):
        scheme, _, token = self.request.headers.get('Authorization', '').partition(' ')

        if scheme.lower() != 'basic':
            return None

        username_or_token, _, pwd_or_userid = token.partition(':')

        # Check in Dynamo
        if pwd:
            user = yield User.verify_pwd(
                username_or_token, 
                pwd_or_userid,
                self.dynamo)

        # Check in Cache
        else:
            user = yield User.verify_token(
                username_or_token,
                pwd_or_userid,
                self.memcache)

        if user:
            return user
        else:
            return None


    """ Helper Function

    """ 

    def _handle_request_exception(self, e):
        err_status, err_msg = request_exception(e)
        self.set_status(err_status)
        self.set_header("Content-Type", "application/json")
        self.finish({'error' : err_msg})

    def write_json(self, data):
        self.set_header("Content-Type", "application/json")
        self.write(json_encode(data))


""" Apply for asynchronous call

"""

def async_login_required(fun):
    @wraps(fun)
    @gen.coroutine
    def __decorator(self, *args, **kw):
        user = yield self.authorize_user()
        if not user:
            self.send_error(403)
            return
        self.current_user = user
        yield fun(self, *args, **kw)

    return __decorator

""" Apply for synchronous call

"""

def login_required(fun):
    @wraps(fun)
    @gen.coroutine
    def __decorator(self, *args, **kw):
        user = yield self.authorize_user()
        if not user:
            self.send_error(403)
            return

        self.current_user = user
        fun(self, *args, **kw)

    return __decorator








