```* here means login required```

#### Friend_Handler

    Add a new friend / test if you two are friend / Delete a friend / Get a list of friend

> post : /api/v1/friend/create

```
PAYLOAD:

        {
            "friend"    :   "a serious user id"
        }
```

> post : /api/v1/friend/test_friend

```
PAYLOAD:

        {
            "friend"    :   "a serious user id"
        }
```

> delete* : /api/v1/friend/delete

```
PAYLOAD:

        {
            "friend"    :   "a serious user id"
        }
```

> get* : /api/v1/friend/get
