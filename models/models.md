## Models

django Documentation study

Models 공부하는 내용들 정리

[Models API](https://github.com/bartkim0426/django-document/blob/master/models/models%20API.md)

공부 더 하고 봐야할듯...

[models field reference]()

field option

표로 정리중. 

Q) choices를 foreignkey에서 받을 수 있나? 

[ForeignKey]()

-> 추후에 정리하기

ManyToMany

-> 추후에 정리, 1107p

[Filed name restrictions]()

Custom field types

-> 추후 정리. Writing custom model fields (p.542)

-> Q) Meta option

metadata: "anything that's not  field" - 필드에 실재하지 않는 메타데이타들.

ex) ordering(ordering), db table name(db_table), human readable name (verbose_name, verbose_name_plural)

[model methods]()

p.94~, p.1136

Q) __eq__(), __hash()__,

[Saving objects, Deleting objects]()

p.1132, p.1135

[Queryset API]()

p.1140~

[Model inheritance]()

p.96~

[Querys]()

[QuerySet API Reference: ]() objects.get()처럼 사용하는 API

[field lookups](): (p.1171) get(), filter(), exclude() 안에 사용되는 lookpus

p.104~

