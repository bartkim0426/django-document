## Methods that return new QuerySets

p.1141

| filter()                                 |      |
| ---------------------------------------- | ---- |
| exclude()                                |      |
| annotate()                               |      |
| order_by()                               |      |
| reverse()                                |      |
| distinct()                               |      |
| values()                                 |      |
| values_list()                            |      |
| dates(field, kind)                       |      |
| datetimes(field_name, kind)              |      |
| none()                                   |      |
| all()                                    |      |
| select_related(*fields)                  |      |
| prefetch_related(*lookups)               |      |
| extra(select=None, where=None, params=None, table=None) |      |
| defer(*fields)                           |      |
| only(*fields)                            |      |
| using(alias)                             |      |
| select_for_update()                      |      |
| raw()                                    |      |
|                                          |      |

### QuerySet을 리턴하지 않는 메소드

| get(**kwargs)              |      |
| -------------------------- | :--- |
| create(**kwargs)           |      |
| get_or_create(**kwargs)    |      |
| update_or_create(**kwargs) |      |
| bulk_create(objs)          |      |
| count()                    |      |
| in_bulk(id_list=None)      |      |
| iterator()                 |      |
| latest(field_name=None)    |      |
| earliest(field_name=None)  |      |
| first()                    |      |
| last()                     |      |
| aggregate()                |      |
| exists()                   |      |
| update(**kwargs)           |      |
| delete()                   |      |
| as_manager()               |      |

#### filter() 

lookup parameter와 매치되는 objects를 담은 쿼리셋을 리턴

lookup param은 반드시 Field lookups에 있는 포맷으로. 여러 파라미터는 AND (__)로 조인 가능하다.

#### exclude()

lookup param과 매치되지 않는 objects를 담은 쿼리셋 리턴. filter와 동일하게 동작.

`Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headlin='hello')`

2005,1,3 이후의 headline이 'hello'인 오브젝트들을 찾는다, SQL 문법으로는 다음과 같다

```sql
SELECT ...
WHERE NOT (pub_date > '2005-1-3' AND headline = 'hello')
```

#### annotate()

p.1142

 query expressions(p.1187) 을 제공하는 쿼리셋 오브젝트

> query expressions: simple value, a reference to a field on the model

? 무슨말인지 잘 모르겠다… 

Annotates each object in the QuerySet with the provided list of query expressions. An expression may be a simple value, a reference to a ﬁeld on the model (or any related models), or an aggregate expression (averages, sums, etc.) that has been computed over the objects that are related to the objects in the QuerySet.

Each argument to annotate() is an annotation that will be added to each object in the QuerySet that is returned.

The aggregation functions that are provided by Django are described in Aggregation Functions below.

Annotations speciﬁed using keyword arguments will use the keyword as the alias for the annotation. Anonymous arguments will have an alias generated for them based upon the name of the aggregate function and the model ﬁeld that is being aggregated. Only aggregate expressions that reference a single ﬁeld can be anonymous arguments. Everything else must be a keyword argument.

#### order_by()

p.1143

모델의 Meta에 있는 ordering 옵션으로 오더링된 쿼리셋이 리턴.

`Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headine')`

=> 'pub_date'로 decending (앞에 -), 'headline'으로 ascending된 결과를 나타냄. 

`Entry.objects.order_by('?')`: ?를 사용하면 randomley order됨. 

다른 모델의 필드로 정렬하려면 더블 언더스코어 (__)를 사용. Meta.ordering이 주어지지 않았으면 primary key로 정렬. 

`Entry.objects.order_by('blog__name', 'headline')`: Blog model의 name으로 정렬

`Entry.objects.order_by('blog')`는 `Entry.objects.order_by('blog__id')`와 같음 (primary key로 정렬됨.)

asc(), decs()와 같은 query expressions도 사용해서 오더링 할수있다. 

`Entry.objects.order_by(Coalesce('summary', 'headline').desc())`이런식으로… 

#### reverse()

queryset의 reverse order를 리턴. 

`my_queryset.reverse()[:5]`: 마지막 5개를 리턴해줌

#### distinct(*fields)

SQL 쿼리로 SELECT DISTINCT를 사용한것같은 쿼리셋을 리턴해준다. 이는 결과에서 duplicate row를 제거한것 (?)

더 공부해야할듯. 무슨말인지 잘...

#### values() p.1146

#### 쿼리셋 dictionary를 반환해줌. 각각의 dict는 모델 오브젝트의 attribute 이름을 key로 갖는다.

```python
>>> Blog.objects.filter(name__startswith='Beatles').values() 
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news. ˓→'}]>
```

옵션으로 value(*fields) 필드명을 받을 수 있다. 그럼 해당 필드만 나옴

```python
>>> Blog.objects.values() 
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news. ˓→'}]>

>>> Blog.objects.values('id', 'name') 
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
```

ForeignKey로 연결된 필드는 id값이 리턴된다. 

```python
>>> Entry.objects.values() 
<QuerySet [{'blog_id': 1, 'headline': 'First Entry', ...}, ...]>

>>> Entry.objects.values('blog') 
<QuerySet [{'blog': 1}, ...]>

>>> Entry.objects.values('blog_id') 
<QuerySet [{'blog_id': 1}, ...]>
```

only(), defer()을 values()와 함께 사용하면 NotImplementedError를 반환한다.

#### values_list()

values()와 비슷하지만 dict를 반환하지 않고 itrated 된 tuple을 반환한다. 

 `flat=True` 파라미터를 추가하면 튜플이 아니라 single value를 반환한다.

```python
>>> Entry.objects.values_list('id').order_by('id') 
[(1,), (2,), (3,), ...]

>>> Entry.objects.values_list('id', flat=True).order_by('id') 
[1, 2, 3, ...]
```

#### dates(field, kind)

datetime.date 오브젝트 리스트를 반환. fiedl에는 DateField의 필드명을, kind에는 "year", "month", "day"중 하나가 들어가야한다. 

각각의 오브젝트는 주어진 타입에 맞는 "truncated"된(잘린? 생략된?) 리스트를 반환한다. `order='DESC'`와 같이 오더링도 가능하다.

```python
>>> Entry.objects.dates('pub_date', 'year') 
[datetime.date(2005, 1, 1)]

>>> Entry.objects.dates('pub_date', 'month') 
[datetime.date(2005, 2, 1), datetime.date(2005, 3, 1)]

>>> Entry.objects.dates('pub_date', 'day') 
[datetime.date(2005, 2, 20), datetime.date(2005, 3, 20)]

>>> Entry.objects.dates('pub_date', 'day', order='DESC') 
[datetime.date(2005, 3, 20), datetime.date(2005, 2, 20)]

>>> Entry.objects.filter(headline__contains='Lennon').dates('pub_date', 'day') [datetime.date(2005, 3, 20)]
```

#### datetimes(field_name, kind, tzinfo=None)

datetime.datetime 오브젝트 리스트를 반환. 

field_name에는 DateTimeField의 이름이 들어가고, kind에는 year, month, day, hour, minute, second 중 하나가 들어감. dates()와 비슷하게 사용 가능. 

tzinfo는 변환될 타임존을 의미. None이면 current time zone을 사용한다. 

#### none()

EmptyQueryset을 반환해준다. 

#### all()

현재 쿼리셋의 copy를 반환. QuerySet이 evaluated 되면 데이터베이스에 영향을 미친다. 

#### select_related(*fields) p.1150

#### prefetch_related(*lookups)

여기부턴 다음에 정리… 너무많다

