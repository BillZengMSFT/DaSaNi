```* here means login required```

#### Client_Handler

    Register an iOS device to SNS App and store information to dynamo User_Apns_SNS_TABLE

> post : /api/v1/client/registry

```
PAYLOAD:

        {
            "deviceToken" : "A serious APNs Token"
        }
```
