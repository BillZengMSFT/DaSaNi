```* here means login required```

#### Auth_Handler

    User log in or log out with push notification re-subscribe or un-subscribe

> post : /api/v1/auth/login

```
PAYLOAD:

        {
            "email"     :   "a serious email end with .edu",
            "password"  :   "a serious password",
            "apns"      :   "device apns token"
        }
```

> delete* : /api/v1/auth/logout

```
PAYLOAD:

        {
            "apns"      :   "device apns token"
        }
```

