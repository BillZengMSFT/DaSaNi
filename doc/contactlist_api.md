```* here means login required```

#### Contactlist_Handler

    Synchronize local contact list to add friends

> post*

```
PAYLOAD:

        {
            "Email"      :   "email address"
            "contacts"    :   [
                {
                    "Email" : "email address or ;",
                    "Phone" : "phone number or ;"
                },
                {
                    "Email" : "email address or ;",
                    "Phone" : "phone number or ;"
                },
                ...
            ]

        }
```

