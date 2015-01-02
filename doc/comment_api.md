```* here means login required```

#### Comment_Handler



> post* : /api/v1/comment/create

        post a new comment.

```
PAYLOAD:
    {
        'event_id'  : 'a serious event id',
        'creator_id': 'a serious user id',
        'content'   : '{
            'type'  : 'text',
            'message' : 'text'
        }"
    }

RETURN:
    {
        'comment_id' : 'comment id',
    }
```
    

> put* : /api/v1/comment/edit

    edit a comment. This method is for future uses.

```
PAYLOAD:
    {
        'comment_id' : 'a serious comment id'
        'content' : 'a serious content'
    }

```

> get* : /api/v1/comment/(event_id)/(timestamp)/(limit)

    Return a group of comments.
    

> delete* : /api/v1/comment/delete

    Remove a comment.

```
	PAYLOAD:
		{
            'comment_id' : 'a serious comment id'
        }

```