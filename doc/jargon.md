***File Name Jargons

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
Modulename.py
```

> /kirin:
```
whatthehell.py
```


***Indentifer Name Jargons

> variable:
```
this_is_a_simple_variable = 1
```

> class:
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

> JSON fields name from client:
```
	{
		"user_id" : "12345",
		"group_id" : "whyyousodiao"
	}
```

> JSON fields name to dynamo:
```
	{
		"UserID" : "12345",
		"GroupID" : "whyyousodiao"
	}
```

> write_json format:
```
	{
		"result" : "ok" or "fail",
		"reason" : "No reason is the best reason" (if "result" is "fail" this field is required)
	}
```