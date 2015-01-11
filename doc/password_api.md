```* here means login required```

#### Password Handler

	

> post : /api/v1/password/send

	send an email which contains activate code for reseting password

```
PAYLOAD:
    {
        "userid": "USERID"
    }
```

> get : /api/v1/password/(userid)/(code)

	verify if a code is valid


> put : /api/v1/password/resend

	resend an email to the user

```
PAYLOAD:
    {
        "userid": "USERID"
    }
```