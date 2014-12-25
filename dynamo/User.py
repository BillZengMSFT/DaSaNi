

from tornado import gen


@gen.coroutine
def verify_pwd(username, pwd, dynamo):
    users = dynamo.get_table('users')
    user = users.get_item(
        username=username,
        password=pwd)
    if user:
        return user['uid']
    else:
        return None

@gen.coroutine
def verify_token(token, userid, memcache):
    if userid in memcache and memcache[userid] == token:
        return userid
    return None