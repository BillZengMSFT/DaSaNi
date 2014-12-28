```* here means login required```

#### Activate Handler

	Activate user accounts, resend activate emails and get activation status

> post : /api/v1/activate

```
PAYLOAD:
    {
        userid: USERID
        code : ACTIVATECODE ## EX: "5DE3C"
    }
```

> put : /api/v1/activate/resend

```
PAYLOAD:
    {
        userid: USERID
    }
```

> get : /api/v1/activated

```
PAYLOAD:
    {
        userid: USERID
    }
```