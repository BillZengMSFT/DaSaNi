```* here means login required```

#### Inbox_Handler

    Create a new inbox message or get a list of current message

> post* : /api/v1/inbox/create

```
PAYLOAD:

        {
            "target_user_id"    :   "a serious user id"
            "payload"   :   "Json information"
        }
```

> get* : /api/v1/inbox/get
