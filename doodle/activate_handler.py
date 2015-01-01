#encoding: utf-8

import tornado
import json
from tornado import gen
from .base_handler import BaseHandler
from .config import *
from .helper import *


class ActivateHandler(BaseHandler):
    @property
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

    @property
    def user_activate_table(self):
        return self.dynamo.get_table(USER_ACTIVATE_TABLE)

    @property
    def user_topic_table(self):
        return self.dynamo.get_table(USER_TOPIC_TABLE)

    @property
    def user_friend_table(self):
        return self.dynamo.get_table(USER_FRIEND_TABLE)

    @property
    def user_event_table(self):
        return self.dynamo.get_table(USER_EVENT_TABLE)

    @gen.coroutine
    def post(self):
        '''
            Get activate code from clients and activate their accounts if a valid code is presented

            PAYLOAD:
            {
                userid: USERID
                code : ACTIVATECODE ## EX: '5DE3C'
            }
        '''
        # read code and userid from json
        code            = self.data['code']
        userid          = self.data['userid']

        # if the code is true then activate the account
        code_is_real    =  self.user_activate_table.has_item(userid)
        if code_is_real:
            activator = yield gen.maybe_future(self.user_activate_table.get_item(userid))
            if activator['Code'] == code:
                user_data = self.user_table.get_item(userid)
                user_data['AccountActive'] = True
                yield gen.maybe_future(user_data.put())
                yield gen.maybe_future(activator.delete())

                # create items in tables for the new account
                new_user_topic_list= self.user_topic_table.new_item(
                    hash_key=hashed_userid,
                    range_key=None,
                    attrs={"TopicList" : ";"}
                    )

                new_user_friend_list= self.user_friend_table.new_item(
                    hash_key=hashed_userid,
                    range_key=None,
                    attrs={"FriendList" : ";"}
                    )

                new_user_event_list = self.user_event_table.new_item(
                    hash_key=hashed_userid,
                    range_key=None,
                    attrs={"EventList" : ";"}
                    )
                yield gen.maybe_future(new_user_topic_list.put())
                yield gen.maybe_future(new_user_friend_list.put())
                yield gen.maybe_future(new_user_event_list.put())


                self.write_json({
                    'result' : 'ok'
                    })

            else:
                # wrong code
                self.write_json_with_status(403,{
                    'result' : 'fail',
                    'reason' : 'authantication failed'
                })
                return


    @gen.coroutine
    def put(self):
        '''
            Request to send a new activate email

            PAYLOAD:
            {
                userid: USERID
            }
        '''
        userid = self.data['userid']
        try:
            # try to retrieve user data and activator
            user_data = yield gen.maybe_future(self.user_table.get_item(userid))
            activator = yield gen.maybe_future(self.user_activate_table.get_item(userid))
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invaild userid'
                })
        # increment on counter
        activator['Attempt'] = activator['Attempt'] + 1
        if activator['Attempt'] > 3:
            # no more than 3 emails per day per user
            self.write_json({
                'result' : 'fail',
                'reason' : 'too many attempts recorded'
            })
            return
        try:
            activate_code = send_email(
                self.ses,
                user_data['Email'],
                user_data['Firstname'],
                user_data['Lastname'])
        except:
            self.write_json({
                'result' : 'fail',
                'reason' : 'failed to send email'
            })
            return

        # update dynamo

        activator['Code'] = activate_code

        yield gen.maybe_future(activator.put())

        self.write_json({
            'result':'ok'
        })


    @gen.coroutine
    def get(self, userid):
        '''
            Retrieve if an account is activated or not
        '''
        try:
            user_data = yield gen.maybe_future(self.user_table.get_item(userid))
        except:
            self.write_json_with_status(400,{
                'result' : 'fail',
                'reason' : 'invalid userid'
                })
        # a simple check on user_data
        if user_data['AccountActive'] == True:
            self.write_json({
                'result' : 'ok'
            })
        else:
            self.write_json({
                'result' : 'fail',
                'reason' : 'account not activated'
            })


