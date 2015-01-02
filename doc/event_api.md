```* here means login required```

#### Event Handler

    Create a new event

> post* : /api/v1/event/create

```
PAYLOAD:
    {
        'name'          : 'a chatgroup name',
        'capacity'      : 'a number of capacity',
        'photo'         : 'a photo url',
        'start_time'    : 'start time, a unix timestamp',
        'end_time'      : 'end time, a unix timestamp',
        'detail'        : 'optional detail about the event',
        'location'      : 'optional location of the event'
    }

RETURN:
    {
        'event_id' : 'event id',
    }
```
    Accept or reject application or invitation / leave / update an event / like an event

> put* : /api/v1/event/put

```
PAYLOAD:
    {
        'type'              : 'application or invitation or leave or update',
        'choice'            : 'accept or deny',
        'event_id'          : 'event to join / like',
        'inbox_message_id'  : 'spcific inbox message id, not required if type is update',
        'who_apply'         : 'optional user who apply for event, required for application',
        'who_invite'        : 'optional user who invite, required for invitation'
        'who_leave'         : 'optional user who leave, required for leave'
        'attrs'             : 'json format string containing new information about this event'
    }

RETURN:
    application / invitation / leave / update/ like

    leave
    {
        'result'    : 'OK'
    }

```

> get : /api/v1/event/(event_id)

> get : /api/v1/event/(event_id)/(timestamp)/(limit)


```
If timestamp and limit is present, then it's fetching a list of events.
Otherwise it's only fetching one event by its event id.

Return specific chatgroup info
    
    {
        'EventID'       : event id,
        'Name'          : event name,
        'CreatorID'     : creator user id,
        'MemberList'    : member list,
        'Capacity'      : a capacity number,
        'PhotoID'       : a photo link,
        'Timestamp'     : timestamp
    }
```


















