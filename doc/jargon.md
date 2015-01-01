#### Filename

> /doc:

```
handler type + _api.md
```

> /doodle:

```
xxx_handler.py
```

> /dynamo:

```
Module.py
```

> /kirin:

```
whatthehell.py
```


#### Indentifer 

> Variable:

```
this_is_a_simple_variable = 1
```

> Function:

```
def this_is_a_good_function(self, some, good=''):
	...
```

> Class:

```
class BeautifulClass(UglyClass):
	...
```

> Constant:

```
WILDCONST = "wow"
```

> Table Names:

```
PINE_TABLE = "Pine_Table"
```

> JSON Field Name From Client:

```
	{
		"user_id" : "12345",
		"group_id" : "whyyousodiao"
	}
```

> JSON Field Name To Dynamo:

```
	{
		"UserID" : "12345",
		"GroupID" : "whyyousodiao"
	}
```

> write_json parameter format:

```
	{
		"result" : "ok" or "fail",
		"reason" : "No reason is the best reason" (if "result" is "fail" this field is required)
	}
```

#### Snippets

```
Bool in dynamo is stored as Number, so NEVER use:
Bad  : ~~some_var is True~~
Good : some_var == True
```

```
Timestamp format:
In comment handler, we don't round it to be integer : 
	str(time.time())
Other places: 
	str(time.time()).split('.')[0]
```

```
List in dynamo:

empty list is ';'

FriendList in user table: userid0;userid1;...
MemberList in event table: userid0;userid1;...
MemberList in chatgroup table: userid0;userid1;...
TopicList in user topic table: sns_topic_0|sub_arn_0;sns_topic_1|sub_arn_1;...

```