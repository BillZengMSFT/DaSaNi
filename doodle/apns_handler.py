#encoding: utf-8

import tornado
from tornado import gen
from .base_handler import BaseHandler
from .helper import *
import config


class APNsHandler(BaseHandler):

    """Incoming JSON

        {
            "token"  : _
        }

        create a new token for the user and register a new sns token

    """

    @gen.coroutine
    def post(self):
       # session check

       # field validation

       response = yield gen.maybe_future(
            self.sns.create_platform_endpoint(
                config.AWS_SNS_IOS_APP_ARN,
                device_token
            )
        )

       # check response

       pass


    @gen.coroutine
    def delete(self):
        pass


















