``` This doc elaborate implementation detail about what each API is doing and what client need to do as a whole system```

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
-> UserHandler          : post /api/v1/user/createx
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
-> mobile send username and passowrd
-> server resubscribe user topic 
```














