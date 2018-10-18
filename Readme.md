based on sqlparse (python)(link https://github.com/PyMySQL/PyMySQL)
```
for 
	- insert
	- update
	- delete
```	

```
expected output 


[
  {
    "rows": "post_id,post_name",
    "values": "1719,"Post 1",
    "optype": "INSERT",
    "table": "posts"
  },
  {
    "where": "WHERE post_id=1719",
    "optype": "DELETE",
    "table": "posts"
  },
  {
    "rows": "post_name=post 2",
    "where": "WHERE id = 1719",
    "table": "posts",
    "optype": "UPDATE"
  }
]


```
