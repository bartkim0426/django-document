## Models

django Documentation study

Models 공부하는 내용들 정리

[Models API](https://github.com/bartkim0426/django-document/blob/master/models/models%20API.md)
공부 더 하고 봐야할듯...

[models field reference](https://github.com/bartkim0426/django-document/blob/master/models/model%20field%20reference.md)

[field option](https://github.com/bartkim0426/django-document/blob/master/models/field%20lookups.markdown)
표로 정리중. 

Q) choices를 foreignkey에서 받을 수 있나? 

[ForeignKey](https://github.com/bartkim0426/django-document/blob/master/models/ForeignKey.md)
-> 추후에 정리하기

[ManyToMany]()
-> 추후에 정리, 1107p

[Filed name restrictions]()


[Custom field types]()
-> 추후 정리. Writing custom model fields (p.542)
metadata: "anything that's not  field" - 필드에 실재하지 않는 메타데이타들.
ex) ordering(ordering), db table name(db_table), human readable name (verbose_name, verbose_name_plural)

[model methods](https://github.com/bartkim0426/django-document/blob/master/models/model%20method.md)
p.94~, p.1136
Q) __eq__(), __hash()__,

[Saving objects, Deleting objects]()
p.1132, p.1135

[Queryset API]()
p.1140~

[Model inheritance]()
p.96~

[Querys](https://github.com/bartkim0426/django-document/blob/master/models/querys.md)

[QuerySet API Reference: ](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown) objects.get()처럼 사용하는 API

[field lookups](https://github.com/bartkim0426/django-document/blob/master/models/field%20lookups.markdown): (p.1171) get(), filter(), exclude() 안에 사용되는 lookpus
p.104~

## Database
[manager](https://github.com/bartkim0426/django-document/blob/master/models/manager.md): p.132~

[raw SQL](https://github.com/bartkim0426/django-document/blob/master/models/SQL.md)

[Database transaction](https://github.com/bartkim0426/django-document/blob/master/models/Database%20transactions.md)

[Multiple database](https://github.com/bartkim0426/django-document/blob/master/models/Multiple%20database.md) : p.153~

[Tablespaces](): p.164~
