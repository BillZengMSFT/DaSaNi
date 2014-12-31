```* here means login required```

#### Chatgroup Handler

    Create a new chatgroup

> post* : /api/v1/chatgroup/create

```
PAYLOAD:
    {
        'eventid'       : 'optional an event id',
        'name'          : 'a chatgroup name',
        'memberlist'    : 'userid_0;userid_1;...',
        'capacity'      : 'a number of capacity',
        'photo'         : 'a photo url'
    }

RETURN:
    {
        'chatgroup_id' : 'chatgroup id',
        'sqs'          : 'sqs arn'
    }
```
    Accept or reject application or invitation / leave

> put* : /api/v1/chatgroup/put

```
Accept or reject application or invitation / leave a chatgroup


PAYLOAD:
    {
        'type'              : 'application or invitation or leave',
        'choice'            : 'accept or deny',
        'chatgroup_id'      : 'chatgroup to join',
        'inbox_message_id'  : 'spcific inbox message id',
        'who_apply'         : 'optional user who apply for chatgroup, required for application',
        'who_invite'        : 'optional user who invite, required for invitation'
        'who_leave'         : 'optional user who leave, required for leave'
    }

RETURN:
    application / invitation
    {
        'sqs'       : 'sqs_arn'
    }

    leave
    {
        'result'    : 'OK'
    }

```

> get : /api/v1/chatgroup/get/chatgroup_id

```
    Return specific chatgroup info
    {
        'ChatgroupID'   : chatgroup id,
        'EventID'       : event id,
        'Name'          : event name,
        'CreatorID'     : creator user id,
        'MemberList'    : member list,
        'Capacity'      : a capacity number,
        'PhotoID'       : a photo link,
        'SQS'           : sqs_arn,
        'Timestamp'     : timestamp
    }
```

> delete : /api/v1/chatgroup/delete

```
PAYLOAD:
    {
        'chatgroup_id'      : 'chatgroup to join',
        'creator_id'        : 'creator user id'
    }
```

















