```* here means login required```

#### Client_Handler

    Register/remove an iOS device to SNS App and store/delete information to dynamo User_Apns_SNS_TABLE

> post* : /api/v1/client/registry

```
PAYLOAD:

        {
            "deviceToken" : "A serious APNs Token"
        }
```

> delete* : /api/v1/client/delete

```
PAYLOAD:

        {
            "deviceToken" : "A serious APNs Token"
        }
```
