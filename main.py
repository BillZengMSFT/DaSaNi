# encoding: utf-8
#   
# web server main app

import os
import tornado.ioloop
import tornado.web
import tornado.options

import functools
import logging
import signal
import time
import boto.sqs
import boto.sns
import boto.ses
import boto.dynamodb
import pylibmc

from tornado.httpserver import HTTPServer

from doodle import *

""" Tornado App Configuration

"""


def get_url_list():

    client_handler_url_set = [
        # register a device to App
        tornado.web.URLSpec(r"/api/v1/client/registry",ClientHandler),
    ]


    user_handler_url_set = [
        # create a new user
        tornado.web.URLSpec(r"/api/v1/user/create",UserHandler),
        # update user info
        tornado.web.URLSpec(r"/api/v1/user/update",UserHandler),
        # get user's info
        tornado.web.URLSpec(r"/api/v1/user/get",UserHandler),
        # get other's info
        tornado.web.URLSpec(r"/api/v1/user/get/(.+)$",UserHandler),
    ]

    activate_handler_url_set = [
        # activate account
        tornado.web.URLSpec(r"/api/v1/user/activate",ActivateHandler),
        # retrieve activation status
        tornado.web.URLSpec(r"/api/v1/user/activated/([0-9A-Za-z]+)",ActivateHandler),
        # resend an activate email
        tornado.web.URLSpec(r"/api/v1/user/activate/resend",ActivateHandler),
    ]

    auth_handler_url_set = [
        # log in
        tornado.web.URLSpec(r"/api/v1/auth/login",AuthHandler),
        # log out
        tornado.web.URLSpec(r"/api/v1/auth/logout",AuthHandler),
    ]

    friend_handler_url_set = [
        # add a new friend
        tornado.web.URLSpec(r"/api/v1/friend/create",FriendHandler),
        # test if someone is a friend
        tornado.web.URLSpec(r"/api/v1/friend/test_friend",FriendHandler),
        # delete a friend
        tornado.web.URLSpec(r"/api/v1/friend/delete",FriendHandler),
        # get a list of current user's friends
        tornado.web.URLSpec(r"/api/v1/friend/get",FriendHandler),
    ]

    inbox_handler_url_set = [
        # create a new inbox
        tornado.web.URLSpec(r"/api/v1/inbox/create",InboxHandler),
        # get a list of current user's message
        tornado.web.URLSpec(r"/api/v1/inbox/get",InboxHandler),
    ]

    chatgroup_handler_url_set = [
        # create a new chatgroup
        tornado.web.URLSpec(r"/api/v1/chatgroup/create",ChatgroupHandler),
        # accept or reject application or invitation / leave
        tornado.web.URLSpec(r"/api/v1/chatgroup/put",ChatgroupHandler),
        # get information about a chatgroup
        tornado.web.URLSpec(r"/api/v1/chatgroup/get/(.*)",ChatgroupHandler),
        # delete a chatgroup
        tornado.web.URLSpec(r"/api/v1/chatgroup/delete",ChatgroupHandler),
    ]

    password_handler_url_set = [
        # create a password activator
        tornado.web.URLSpec(r"/api/v1/password/send",PasswordHandler),
        # verify a password code
        tornado.web.URLSpec(r"/api/v1/password/verify",PasswordHandler),
        # resend email
        tornado.web.URLSpec(r"/api/v1/password/resend",PasswordHandler),
    ]

    url_list = [
        client_handler_url_set,
        user_handler_url_set,
        activate_handler_url_set,
        auth_handler_url_set,
        friend_handler_url_set,
        inbox_handler_url_set,
        chatgroup_handler_url_set,
        password_handler_url_set
    ]

    url_full_list = []

    for url_set in url_list:
        for url in url_set:
            url_full_list.append(url)

    return url_full_list


def get_settings():

    return {
        'login_url': '/api_v1/login',
        'debug': True
    }


def get_sqs():
    
    conn = boto.sqs.connect_to_region(
        'us-west-2',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_ACCESS_KEY)
    return conn

def get_dynamo():
   
    conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_ACCESS_KEY)
    return conn

def get_sns():

    conn = boto.sns.connect_to_region(

        config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_ACCESS_KEY)
    return conn

def get_ses():

    conn = boto.ses.connect_to_region(
        config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_ACCESS_KEY)
    return conn

def get_dynamo():

    conn = boto.dynamodb.connect_to_region(
        config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_ACCESS_KEY)

    return conn


def get_memcache():
    return pylibmc.Client(
        [config.MEMCACHE_ADDRESS], 
        binary=True, 
        behaviors={
        "tcp_nodelay": True,
        "ketama": True})

def get_app():

    url_list = get_url_list()
    settings = get_settings()
    sqs = get_sqs()
    sns = get_sns()
    dynamo = get_dynamo()
    memcache = get_memcache()
    
    application = tornado.web.Application (
        url_list,
        sqs = sqs,
        sns = sns,
        ses = ses,
        dynamo = dynamo,
        memcache = memcache,
        **settings
    )
    
    return application

def get_ioloop():

    ioloop = tornado.ioloop.IOLoop.instance()
    return ioloop


def stop_server(server):

    logging.info('--- stopping club server ---')
    server.stop()


""" SSL not implemented yet

"""

def get_ssl():

    data_dir = '../'

    return {
                "certfile": os.path.join(data_dir, "server.crt"),
                "keyfile": os.path.join(data_dir, "server.key")
           }


""" Tornado server run loop
    
"""

def main():

    application = get_app()
    tornado.options.parse_command_line()
    server = HTTPServer(application)#, ssl_options=get_ssl())
    server.listen(80)
    ioloop = get_ioloop()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        stop_server(server)

    logging.info('--- club server stopped ---')


if __name__=='__main__':
    main()


