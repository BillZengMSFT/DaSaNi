#encoding: utf-8

import tornado
import time
import re
from .config import *
from tornado import gen
from .base_handler import *
from .helper import *
from boto.dynamodb.condition import *
from operator import attrgetter

class CommentHandler(BaseHandler):

    @property 
    def event_comment_table(self):
        return self.dynamo.get_table(EVENT_COMMENT_TABLE)

    @async_login_required
    @gen.coroutine
    def post(self):
        """
            post a new comment on a event
        """
        if len(client_data["content"]) >= 200:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'content too long'
                })
        client_data = self.data
        now = str(time.time())
        comment_id = md5(client_data['content']+now)

        attrs = {
            'CommentID' : comment_id,
            'CreatorID' : creator_id,
            'Content'   : content,
            'EventID'   : event_id,
            'Timestamp' : now
        }

        new_comment = self.event_comment_table.new_item(
            hash_key=comment_id,
            attrs=attrs)
        new_comment.put()

        self.write_json({
            'comment_id' : comment_id
            })
        

    @async_login_required
    @gen.coroutine
    def put(self):
        """
            Firewall needed to filter out invalid fields.
            update a comment. reserved for later use.
            PAYLOAD:
            {
                'comment_id' : 'a serious comment id'
                'content' : 'a serious content'
            }
        """
        client_data = self.data
        try:
            comment = self.event_comment_table.get_item(client_data['comment_id'])
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid comment id'
                })
        if self.current_userid != comment["CreatorID"]:
            self.set_status(403)
            self.write_json({
                'result' : 'fail',
                'reason' : 'Anthantication failed'
                })
        comment['Coentent'] = client_data['data']
        comment['Timestamp'] = str(time.time())
        comment.put()
        self.write_json({
            'comment_id' : comment_id,
            'Timestamp' : comment['Timestamp']
            })


    @async_login_required
    @gen.coroutine
    def delete(self):
        """
            delete a specific comment
            PAYLOAD:
            {
                'comment_id' : 'a serious comment id'
            }
        """
        client_data = self.data
        try:
            comment = self.event_comment_table.get_item(client_data['comment_id'])
        except:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'invalid comment id'
                })
        if self.current_userid != comment["CreatorID"]:
            self.set_status(403)
            self.write_json({
                'result' : 'fail',
                'reason' : 'Anthantication failed'
                })
        comment.delete()
        self.write_json({
            "result" : 'ok',
            })


    @async_login_required
    @gen.coroutine
    def get(self):
        """
            get a specific comment
            PAYLOAD:
            {
                'limit'      : 'the limit of number of comments',
                'timestamp'  : 'a serious timestamp',
                'event_id'   : 'a serious eventid'
            }
        """
        # ensure that limit is an integer!!!
        limit = int(limit)
        if limit<= 10 or limit >= 20:
            self.set_status(400)
            self.write_json({
                'result' : 'fail',
                'reason' : 'limit is too high or too low'
                })
        comments = self.event_comment_table.scan(
            {
            'EventID' : EQ(client_data['event_id']),
            'Timestamp' : LE(client_data['timestamp'])
            },
            max_result=limit
            )
        response = []
        for comment in comments:
            response.append(comment)
        if len(response) == 0:
            self.write_json({
            'result' : response,
            })
        else:
            response = sorted(response,key=attrgetter('Timestamp'),reverse=True)
        self.write_json({
            'result' : response,
            'new_timestamp' : response[-1]['Timestamp']
            })
