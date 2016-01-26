#encoding: utf-8

import tornado
import json
from tornado import gen
from .base_handler import BaseHandler
from .config import *
from .helper import *
from boto.dynamodb2.table import Table

class PasswordHandler(BaseHandler):
    @property
    def user_table(self):
        return Table('User_Table',connection=self.dynamo)

    @property
    def user_activate_table(self):
        return Table('User_Activate_Table',connection=self.dynamo)

    @gen.coroutine
    def post():
        """
            send an activate code to user's email and make an record in User_Activate_Table
            PAYLOAD:
            {
                "userid":"a serious user id"
            }
        """
        client_data = self.data
        userid = client_data['userid']
        try:
            # fetch user data from dynamodb
            user = yield gen.maybe_future(self.user_table.get_item(UserID=userid))
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid userid'
            })
        try:
            # generate activate code and send email
            activate_code = yield gen.maybe_future(
                send_email(
                    self.ses,
                    user["Email"],
                    user["FirstName"],
                    user["LastName"]
                )
            )
        except:
            # process exception
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'failed to send email'
            })
        
        # save activator code to dynamodb
        yield gen.maybe_future(
            self.user_activate_table.put_item(data={
                "UserID"    : userid,
                "Timestamp" : str(time.time()).split(".")[0],
                "Code"      : activate_code,
                "Attempt"   : 1
                })
        )

        self.write_json({
            'result': 'ok',
        })

    @gen.coroutine
    def get(userid, code):
        """
            verify code from client
        """
        try:
            activator = yield gen.maybe_future(self.user_activate_table.get_item(UserID=userid))
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid userid'
            })
        if code == activator["Code"]:
            self.write_json({
            'result': 'ok',
            })
        else:
            # wrong code
            self.write_json_with_status(403,{
                'result' : 'fail',
                'reason' : 'authantication failed'
            })

    @gen.coroutine
    def put():
        """
            resend email.
            PAYLOAD:
            {
                "userid": "a serious user id"
            }
        """
        try:
            activator = yield gen.maybe_future(self.user_activate_table.get_item(UserID=userid))
            user = yield gen.maybe_future(self.user_table.get_item(UserID=userid))
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid userid'
            })

        # increment on counter
        activator['Attempt'] = activator['Attempt'] + 1
        if activator['Attempt'] > 3:
            # no more than 3 emails per day per user
            self.write_json({
                'result' : 'fail',
                'reason' : 'too many attempts recorded'
            })

        try:
            # generate a new activate code and send email
            activate_code = yield gen.maybe_future(
                send_email(
                    self.ses,
                    user["Email"],
                    user["FirstName"],
                    user["LastName"]
                )
            )
        except:
            # process exception
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'failed to send email'
            })

        activator['Code'] = activate_code

        yield gen.maybe_future(activator.partial_save())

        self.write_json({
            'result':'ok'
        })