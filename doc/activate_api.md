```* here means login required```

#### Activate Handler

	Activate user accounts, resend activate emails and get activation status

> post : /api/v1/user/activate

```
PAYLOAD:
    {
        "user_id": "USERID"
        "code" : "ACTIVATECODE" ## EX: "5DE3C"
    }
```

> put : /api/v1/user/activate/resend

```
PAYLOAD:
    {
        "user_id": "USERID"
    }
```

> get : /api/v1/user/activated/(uid)

```
    Return whethere an given uid is activated or not
```