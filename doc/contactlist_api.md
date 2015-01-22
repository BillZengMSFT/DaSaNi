```* here means login required```

#### Contactlist_Handler

    Synchronize local contact list to add friends

> post*

```
PAYLOAD:

        {
            "UserID"    :   "UserID"
            "Email"      :   "email address"
            "contacts"    :   [
                {
                    "Email" : "email address",
                    "Phone" : "phone number"
                },
                {
                    "Email" : "email address",
                    "Phone" : "phone number"
                },
                ...
            ]

        }
```

