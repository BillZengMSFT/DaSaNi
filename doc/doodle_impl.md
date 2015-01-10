```This doc elaborate implementation detail about what each API is doing and what client need to do as a whole system```

##### Device Reigstry

> Process

```
-> mobile open everytime register
```

> API Call

```
-> ClientHandler        : post /api/v1/client/registry
```

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
-> EventHandler         : get /api/v1/event/(event_id)/(timestamp)/(limit)
```

##### Create An Event

> Process

```
-> mobile create a new event
```

> API Call

```
-> EventHandler         : post /api/v1/event/create
```

##### Like An Event

> Process

```
-> mobile like a event
```

> API Call

```
-> EventHandler         : put /api/v1/event/put
```

##### View An Event

> Process

```
-> mobile view an event
```

> API Call

```
-> EventHandler         : get /api/v1/event/(event_id)
```

##### Comment An Event

> Process

```
-> mobile comment an event
```

> API Call

```
-> CommentHandler       : post /api/v1/comment/create
```

##### Join An Event

> Process

```
-> mobile confirm join an event in inbox or apply in event view
```

> API Call

```
-> EventHandler         : put /api/v1/event/put
```

##### Share An Event

> Process

```
-> mobile share to friend or other sns
```

> API Call

```
-> mobile make a piece of message customized for different use
```

##### View Like People List

> Process

```
-> mobile view people list who like it
```

> API Call

```
-> grab the event directly
```

##### View Friends Who Join

> Process

```
-> mobile view people list who join intersects with local friend database
```

> API Call

```
-> grab the event directly
```

##### Leave An Event

> Process

```
-> mobile leave an event
```

> API Call

```
-> EventHandler         : put /api/v1/event/put
```

##### Apply For Chatgroup In Event

> Process

```
-> mobile apply for chatgroup
```

> API Call

```
-> EventHandler         : put /api/v1/event/put

On other phone
-> InboxHandler         : post /api/v1/inbox/get
```

##### Invite To Chatgroup In Event

> Process

```
-> mobile invite to chatgroup (friends or people who joined this event)
```

> API Call

```
-> InboxHandler         : post /api/v1/inbox/create

On other phone
-> EventHandler         : put /api/v1/event/put
```

##### View People Who Join

> Process

```
-> mobile view people list who join
```

> API Call

```
-> grab the event directly
```

##### Create An Event

> Process

```
-> mobile create an event
```

> API Call

```
-> EventHandler         : post /api/v1/event/create
```

##### View Inbox

> Process

```
-> mobile view inbox
```

> API Call

```
-> InboxHandler         : get /api/v1/inbox/get
```

##### Send Messages To Inbox

> Process

```
-> mobile make a payload for customized use
```

> API Call

```
-> InboxHandler         : post /api/v1/inbox/create
```

##### Create A Chatgroup

> Process

```
-> mobile create a chatgroup
```

> API Call

```
-> ChatgroupHandler     : post /api/v1/chatgroup/create         
```

##### Edit A Chatgroup

> Process

```
-> mobile edit a chatgroup
```

> API Call

```
-> ChatgroupHandler     : put /api/v1/chatgroup/put
```

##### Chat In Chatgroup

> Process 

```
-> mobile publish to chatgroup
```

> API Call

```
-> mobile publish to specific sqs
```

##### Join A Chatgroup

> Process

```
-> mobile join a chatgroup
```

> API Call

```
-> ChatgroupHandler     : put /api/v1/chatgroup/put
```

##### Leave A Chatgroup

> Process

```
-> mobile leave a chatgroup
```

> API Call

```
-> ChatgroupHandler     : put /api/v1/chatgroup/put
```

##### Dismiss A Chatgroup

> Process

```
-> mobile delete a chatgroup
```

> API Call

```
-> ChatgroupHandler     : delete /api/v1/chatgroup/delete
```

##### Kickout A Person In Chatgroup

> Process

```
-> mobile let someone leave a chatgroup
```

> API Call

```
-> ChatgroupHandler     : put /api/v1/chatgroup/put
```


##### Make A Friend

> Process

```
-> mobile accept application in inbox
```

> API Call

```
Who ask you:
-> InboxHandler         : post /api/v1/inbox/create

Who decide:
-> FriendHandler        : post /api/v1/friend/create
```

##### Delete A Friend :(

> Process

```
-> mobile delete a friend
```

> API Call

```
-> delete local db
-> FriendHandler        : delete /api/v1/friend/delete
```

##### View Friend List

> Process

```
-> mobile get friend list
```

> API Call

```
-> FriendHandler        : get /api/v1/friend/get
-> mobile store to local db
```

