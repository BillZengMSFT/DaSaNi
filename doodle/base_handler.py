#encoding: utf-8

import tornado
import json




class BaseHandler(tornado.web.RequestHandler):

    @property
    def sqs(self):
        return self.settings['sqs']

    @property 
    def sns(self):
        return self.settings['sns']

    @property
    def data(self):
        return json.loads(self.request.body.decode('utf-8'))
