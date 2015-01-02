```This doc elaborate implementation detail about what each API is doing and what client need to do as a whole system```

##### User Registry

> Process

```
-> mobile Post {email, firstname, lastname} 
-> Receive email 
-> mobile Put activate code to activate 
-> mobile Put {password}
-> mobile register 
```

> API Call

```
-> UserHandler          : post /api/v1/user/create
-> Helper Function      : send an email over SES 
-> Put an activation code in table (24h expires -> towelpaper service background check, user will be deleted)
-> ActivateHandler      : post /api/v1/user/activate 
-> UserHandler          : put  /api/v1/user/update
```

##### User Reset Password

> Process

```
-> mobile resend activation email
-> Receive email
-> mobile Post activate code to activate
-> mobile Put {password}
```

> API Call

```
-> ActivateHandler      : put /api/v1/user/activate/resend
-> Helper Function      : send an email over SES 
-> Put an activation code in table (24h expires -> towelpaper service background check, user won't be deleted)
-> ActivateHandler      : post /api/v1/user/activate 
-> UserHandler          : put  /api/v1/user/update
```

##### User Login

> Process

```
-> mobile type in password and email
-> mobile md5 email -> userid
-> mobile test if user is active -NO-> ask for activate code
-> mobile login
```

> API Call

```
ActivateHandler         : get /api/v1/user/activated/(uid)
AuthHandler             : post /api/v1/auth/login
```

##### User Logout

> Process

```
-> mobile logout
```

> API Call

```
-> AuthHandler          : delete /api/v1/auth/logout
```

##### View Event List

> Process

```
-> mobile view event list
```

> API Call

```
-> 
```

##### Create An Event

##### Like An Event

##### View An Event

##### Comment An Event

##### Join An Event

##### Share An Event

##### View Like People List

##### View Friends Who Join

##### Leave An Event

##### Apply For Chatgroup In Event

##### Invite To Chatgroup In Event

##### View People Who Join

##### Create An Event

##### View Inbox

##### Send Messages To Inbox

##### Create A Chatgroup

##### Chat In Chatgroup

##### Join A Chatgroup

##### Leave A Chatgroup

##### Dismiss A Chatgroup

##### Kickout A Person In Chatgroup

##### Make A Friend

##### Delete A Friend :(

##### View Friend List

##### Register A Device





























