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
    def user_table(self):
        return self.dynamo.get_table(USER_TABLE)

    @property 
    def user_inbox_table(self):
        return self.dynamo.get_table(USER_INBOX_TABLE)

    @property
    def event_table(self):
        return self.dynamo.get_table(EVENT_TABLE)

    @property
    def user_event_table(self):
        return self.dynamo.get_table(USER_EVENT_TABLE)

    """
        Create a new event
    """

    @async_login_required
    @gen.coroutine
    def post(self):
        client_data = self.data
        timestamp = str(time.time()).split('.')[0]
        event_id = md5(self.current_userid + 'event' + timestamp)
        if self.current_userid == ADMIN_USERID:
            official = True
        else:
            official = False
        attrs = {
            'EventID'       : event_id,
            'Name'          : client_data['name'],
            'CreatorID'     : self.current_user,
            'MemberList'    : client_data['memberlist'],
            'LikeList'      : ';',
            'detail'        : sns_arn,
            'location'      : sqs_arn,
            'Timestamp'     : timestamp,
            'StartTime'     : client_data['start_time'],
            'EndTime'       : client_data['end_time'],
            'PhotoID'       : client_data['photo'],
            'Capacity'      : client_data['capacity'],
            'Official'      : official
        }
        new_event = self.event_table.new_item(
            hash_key = event_id,
            range_key = None,
            attrs = attrs
            )
        new_event.put()
        self.write_json({
            'event_id' : event_id
            })

    """
        accept application / accept invitation / leave/ update/ like
    """
    @async_login_required
    @gen.coroutine
    def put(self):
        client_data = self.data
        request_type = client_data['type']
        choice = client_data['choice']
        event_id = client_data['event_id']
        inbox_id = client_data['inbox_message_id']
        if request_type == 'application':
            self.__event_application(client_data['who_apply'], event_id, self.current_userid, choice, inbox_message_id)
        elif request_type == 'invitation':
            self.__event_invitation(client_data['who_invite'], event_id, self.current_userid, choice, inbox_message_id)
        elif request_type == 'leave':
            self.__event_leave(client_data['who_leave'], event_id, inbox_message_id)
        elif request_type == 'update':
            self.__event_update(client_data['attrs'], event_id)
        elif request_type == 'like':
            self.__event_like(self.current_userid, event_id)
        self.write_json({
            'result' : 'ok'
            })


    def __event_application(self,who_apply,event_id,who_decide,choice, inbox_message_id):
        if choice == "accept":
            try:
                event = self.event_table.get_item(event_id)
            except:
                self.set_status(400)
                self.write_json({
                    'result' : 'fail',
                    'reason' : 'invalid event id'
                    })
            if re.search(who_apply, event['MemberList']) == None:
                event['MemberList'] = list_append_item(event['MemberList'], who_apply)

                # delete inbox message
                try:
                    inbox_message = self.user_inbox_table.get_item(inbox_message_id)
                except:
                    self.set_status(400)
                    self.write_json({
                        'result' : 'fail',
                        'reason' : 'invalid inbox id'
                        })
                inbox_message.delete()
                
            else:
                self.set_status(400)
                self.write_json({
                    'result' : 'fail',
                    'reason' : 'user already joined'
                    })
    """
        It is same with application, who_invite has no action, 
        but who_decide has same action with who_apply
    """

    def __event_invitation(self, who_invite, event_id, who_decide, choice, inbox_message_id):
        self.__event_application(who_decide, event_id, who_decide, choice, inbox_message_id)

            
    def __event_leave(self, who_leave, event_id, inbox_message_id):
        try:
            event = self.event_table.get_item(event_id)
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid event id'
                })
        if re.search(who_leave, event['MemberList']) != None:
            event['MemberList'] = list_delete_item(who_leave + ".*?;", event['MemberList'])
            event.put()

        # delete inbox message
        try:
            inbox_message = self.user_inbox_table.get_item(inbox_message_id)
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid message id'
            })
        inbox_message.delete()
        self.write_json({'result' : 'OK'})



    def __event_update(self, attrs, event_id):
        self.input_firewall(attrs)
        try:
            event = self.event_table.get_item(event_id)
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid event id'
            })
        event.update(attrs)
        event.put()
        self.write_json({'result' : 'OK'})



    def __event_like(self, current_userid, event_id):
        try:
            event = self.event_table.get_item(event_id)
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid event id'
            })
        if re.search(current_userid, event['LikeList']) == None:
            event['LikeList'] = list_append_item(current_userid, event['LikeList'])
            event.put()
            self.write_json({
                'result' : 'ok'
            })
        else:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'user already in the like list'
            })




    """
        Get specific event info
    """

    @async_login_required
    @gen.coroutine
    def get(self, event_id=''):
        response = {}
        try:
            event = self.event_table.get_item(event_id)
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid event id'
                })
        for key, val in event.itmes():
            response[key] = val
        self.write_json(response)


