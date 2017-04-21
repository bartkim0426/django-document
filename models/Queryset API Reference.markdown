## Queryset API reference

### When QuerySets are evaluated (p.1140)

언제 queryset이 evaluated 되는지 (이거 정리한거같은데...)

- **iteration**
- **slicing**
- **pickling/Caching**
- **repr()**
- **len()**
- **list()**
- **bool()**

#### Pickling QuerySets (p.1141)

1141.p 참고



### Methods that return new QuerySets

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

쿼리에서 실행된 추가적인 related-object data를 따르는 foreign-key 관계를 따르는 쿼리셋을 리턴 (??)

=> 성능 부스터됨: 나중에 foreign-key relationship이 db query에서 필요가 없을 경우에… (???)

예시 (일반 lookup과 select_related() lookup의 차이)

```python
# 일반적인 lookup
e = Entry.objects.get(id=5)

b = e.blog # related된 Blog object를 얻기 위해 db를 한 번 더 hit

# select_related lookup
e = Entry.objects.select_related('blog').get(id=5)

b = e.blog 
# 똑같아 보이지만 이전 쿼리에서 e.blog가 이미 뽑혔기 때문에 db를 hit하지 않는다
```

어떤 쿼리셋에서든지 `select_related()` 를 사용 가능하다.

```python
from django.utils import timezone

# 미래에 published되게 스케쥴링된 entries를 찾기
blog = set()

for e in Entry.objects.filter(pub_date__gt=timezone.now()).select_related('blog'):
    blog.add(e.blog)
    # select_related()가 없으면, 각각의 loop iteration에서 db를 hit한다.
```

다음의 예시에서 foreignkey도 같은 방식임을 확인할 수 있다.

```python
from django.db import models

class City(models.Model):
    ...
    pass

class Person(models.Model):
    ...
    hometown = models.ForeignKey(
    	City,
        ...,
    )

class Book(models.Model):
    ...
    author = models.ForeignKey(Person)
```

이제 `Book.objects.select_related('author__hometown').get(id=4)` 는 Person, City와 모두 연관된 값을 캐싱한다.

```python
b = Book.objects.select_related('author__hometown').get(id=4)
p = b.author 
c = p.hometown
# select_related로 뽑았기 때문에 위의 p, c 모두 db를 hit하지 않는다.

b = Book.objects.get(id=4)
p = b.author
c = p.hometown
# 둘 다 db를 hit한다.
```

어떤 ForeignKey나 OneToOneField 관계에서든지 select_related()를 사용 가능하다. 

이미 불러진 QuerySet list를 clear하기 위해서는 None을 파라미트로 주면 된다.

```python
>>> without_relations = queryset.select_related(None)
```

select_related는 Chaining도 가능하다 - `select_related('foo', 'bar')` 과 같이...

자세한 내용은 doc 참고...



#### prefetch_related(*lookups)

> prefetch: 진행중인 처리와 병행하여 필요하다고 생각되는 명령 또는 데이터를 사전에 판독하는 것

"Returns a QuerySet that will automatically retrieve, in a single batch, related objects for each of the speciﬁed lookups." (잘 해석이 안돼요..) 

위의 select_related과 비슷하지만 foreign-key, Ono-to-one 뿐 아니라 many-to-many 등 모든 relations에서 사용 가능하다…는 것 만 알겠다 (나머지는 doc 참고)

```python
from django.db import models

class Topping(models.Model):
    name = models.CharField(max_length=30)
    
class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)
    
    def __str__(self):
        return "%s (%s)" %(
        	self.name,
            ", ".join(topping.name for topping in self.topping.all())
        )
```

이런 모델에서 다음 쿼리문을 비교해보았다.

```python
>>> Pizza.objects.all()
# 위 구문은 매 object마다 Pizza.__str__()을 실행하면서 self.topping.all()을 실행. 
>>> Pizza.objects.prefetch_related('toppings')
# 위와 달리 self.toppings.all()이 실행되면 이미 prefetch된 QuerySet의 캐시에서 싱글 쿼리를 뽑아낸다.
```



더 자세한 내용은 doc...



#### extra() (p.1155)

여기부턴 다음에 정리… 너무많다

...

#### defer(\**fields*) : p.1158 

Q) 잘몰겠음… 특정 필드의 로드를 늦춰주는?

복잡한 data-modeling 상황에서, 모델은 많은 필드를 포함하고 있다: 많은 데이터가 있는 필드 (text field같이)나 Python object로 변환해주는 프로세싱을 필요로 하는 필드 등… 

만약 쿼리셋 결과를 사용하기 위해 처음 data를 fetch 할 때 특정 필드가 필요 없다고 생각되면 django에게 retrieve 하지 말라고 할 수 있음: defer()를 사용해서 load하지 않을 필드를 특정 가능하다.

```python
Entry.objects.defer("headline", "body")
```

그래도 model instance를 리턴하긴 함: 각각의 deferred field는 필드에 접근 할 때 db에서 retrieved 된다. 

다음과 같이 여러번 부를 수도 있다.

```python
Entry.objects.defer("body").filter(rating=5).defer("headline")
```

related models의 필드 또한 defer 가능하다

```python
Blog.objects.select_related().dfer("entry__headline", "entry__body")
```

모든 deferred fields를 지우려면 None을 파라미터로 주면 된다.

```python
my_queryset.defer(None)
```

몇몇 필드들은 defer되지 않는다: primary key는 결코 defer할 수 없음, 에러를 반환한다.

> defer(), only()는 advanced use-case: 최적화를 해주지만 당신이 어떤 정보를 원하고, 전체 데이터 셋을 뽑아내는것과 명확히 어떤 차이가 있는지 '정확히' 알고 사용해야한다… ㄷㄷㄷ 자세한 내용은 공식 문서 (p.1159) 참고

#### only(\**fields*): p.1160

only 메소드는 defer()과 반대되는 개념. 모델을 retrieving 할 때 defer되지 않을 필드를 명시. 다음과 같이 defer()과 함께 사용 가능하다.

```python
# This will defer all fields except the headline. 
Entry.objects.only("body", "rating").only("headline")

# Final result is that everything except "headline" is deferred
Entry.objects.only("headline", "body").defer("body")

# Final result loads headline and body immediately (only() replaces any 
# existing set of fields).
Entry.objects.defer("body").only("headline", "body")
```

자세한 내용은 공식 문서.



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

