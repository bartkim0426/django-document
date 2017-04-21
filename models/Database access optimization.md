## Database accss optimization (최적화)

장고의 db layer는 다양한 방법으로 개발자들이 db에 접근하게 도와줌: 여러 연관된 다큐멘트, 다양한 팁, 많은 아웃라인들을 모아놓음

#### Profile first: 무슨 뜻인지 잘.. Q)

*what queries you are doing and what they are costing you* (p.621. Db and models FAQ) 읽어보기

django-debug-toolbar를 사용하면 db를 바로 모니터링 할 수 있음

optimizing은 누군가에게는 detrimental이 될 수 있다 -> priorities를 결정하고 balance를 생각하는것 등…은 자신의 application, server에 달렸다: 

(이런 일련의 과정을 프로파일 하는것?을 profile이라고 부르는 것 같습니다…)

=> 아래 나오는 **모든** 제안들은 상황에 따라서 general principle로 적용 될수도, 아닐수도 있다.

#### Use standard DP optimization techniques

…including:

- Index: 어떤 index들이 올 지 profiling 한 이후에 가장 중요한 우선순위. 

  `Field.db_index` 혹은 `Meta.index_together`를 사용하여  추가.

  자주 사용하는 query에 대해 filter(), exlude(), order_by() 등을 사용할 때 index를 추가한다고 생각하면 lookup(찾아볼 때) 할 때 도움이 많이 된다. 

- Appropriate use of filed types (적절한 필드 타입)



위의 내용은 명백하다. 나머지 이 문서는 Django를 사용할 때 필요없는 (unnecessary) 작업을 하지 않는데에 초점: 모든 operation에 적용되지 않을 수 있다. (general purpose caching-p.405처럼)

#### Understand QuerySets

[QuerySets](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown)을 이해하는 것은 간단한 코드에서 좋은 성능을 내는데 중요하다. 특히:

##### Understand QuerySet evaluation

성능의 문제를 피하기 위해서 다음이 중요하다

- *[QuerySets are lazy](https://github.com/bartkim0426/django-document/blob/master/models/querys.md#querysets-are-lazy)* : p.107
- *[they are evaluated](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#when-querysets-are-evaluated-p1140)*: p.1139
- how *[the data is held in memory]()*: p.113. 아직 못 읽음...

#### Understanding cached attributes

QuerySet 전체를 부르면 전체 결과에 caching이 된다.

```python
>>> entry = Entry.objects.get(id=1)
>>> entry.blog # Blog object가 여기서 불러짐
>>> entry.blog # cache된 버전, DB 접근은 아니다

# attribute를 부르면 매번 DB를 lookup한다
>>> entry.authors.all() # query가 실행됨
>>> entry.authors.all() # query가 다시한번 실행된다
```

template code에서 주의: template 시스템은 위의 차이를 숨기고 그냥 부를 수 있는 객체를 자동으로 부름 (parenthese-삽입구?를 허용하지 않는다? 무슨말이지… 아마 아래의 with tag와 관련이 있는 것 같다.)

own custom properties에서도 주의: 필요할 때 caching 도구를 활용하는 것은 자기에게 달려있다. ex) `cached_property` decorator 처럼…(p.1368)

##### Use the 'with' template tag

QuerySet의 caching behavior를 사용하기 위해서 `with` 템플릿 태그를 사용하면 된다.

##### Use iterator()

objects가 많은 경우에, QuerySet을 캐싱하는 건 많은 메모리 소모: 이 경우 `iterator()`(p.1166)를 사용하는 것이 도움됨.

#### Do database work in the db rather than in Python

예를들면

- 대부분의 기본 레벨에서: db를 필터링 하기 위해 *[filter and exclude](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#filter)*를 사용
- 같은 모델 안 다른 필드를 필터하기 위해 *[F expressions]()*(p.1188, 따로 정리 필요)을 사용
- *annotate to do aggregation in the database*를 사용 (p.122, 따로 정리 필요)

이것들이 SQL을 만들어내는데 불충분하다면 다음이 필요하다:

##### Use RawSQL

편리하지는 않지만 더 강력한 방법들이 *RawSQL*(p.1193, 따로 정리 필요. `class RawSQL`)에서 가능하다. 

##### Use raw SQL

자신만의 *[custom SQL to retrieve data](https://github.com/bartkim0426/django-document/blob/master/models/SQL.md)*(p.137)를 사용. `django.db.connection.queries`를 사용해서 장고가 어떤  query를 제공하는지를 확인하고 거기서 시작하면 된다.

##### Retrieve individual objects using a unique, indexed column

*unique*, *db_index* (p.1090~1091)를 칼럼에 사용하는 데에는 두가지 이유가 있다.

1. underlying db index가 있으면 더 빠르게 찾을 수 있음

> Field.db_index: if True, db index will be created for this field

2. multiple objects가 매칭되면 더 느리게 동작: unique하다는 제약은 이런 일이 일어나지 않을거라고 보증

```python
>>> entry = Entry.objects.get(id=10) 
>>> entry = Entry.objects.get(headline="News Item Title")
```

위의 예시에서 첫번째가 두번째보다 빠름: id가 db에서 unique하다고 보장되기 때문에!

##### Retrieve everything at once if you knwo you will need it

여러 번의 single data set을 통해 db를 여러번 접근하는 것은 보통 한번에 모든 쿼리를 가져오는 것보다 느리다: 만약 많은 db query들이 필요하다면, 한번에 가져오는 것이 좋다, So:

##### Use QuerySet.select_related() and prefetch_related() (잘 이해가 안됨)

*[select_related](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#select_relatedfields-p1150)*와 *[prefetch_related](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#prefetch_relatedlookups)*를 완전히 이해하고, 이들을

- view code와
- 적절한 *managers and default managers*에서 사용해라. 

[select_related, prefetch_related를 잘 설명해 놓은 블로그](http://jupiny.tistory.com/entry/selectrelated%EC%99%80-prefetchrelated)

#### Don't retrieve things you don't need

##### Use QuerySet.values() and values_list()

value의 dict, list만 필요할 때는 ORM model object가 필요 없다. *[values()](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#values-p1146)*의 적절한 활용이 필요하다: 이는 model objects를 템플릿 코드에 사용할 때 유용

##### Use QuerySet.defer() and only()

만약 필요하지 않은 db columns을 명확히 알고 있다면 그들을 로딩하지 않기 위해  *[defer()](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#deferfields--p1158)*, *[only()](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#onlyfields-p1160)* 를 사용할 수 있다. 

장고가 deferred field를 만들 때 조금의 overhead가 발생: non-text, non-VARCHAR data 등에 너무 공격적으로 사용하지 말것. 주로 많은 text data를 로딩하는 것을 피할 때 유용하게 쓰인다. 

> "**As always, profile first, then optimize**" (profile이 도대체 어떤거지)

##### Use QuerySet.count()

…수를 세고 싶다면, len(queryset)보다 count가 낫대

##### Use QuerySet.exists()

…만약 결과가 존재하는지 알고 싶다면 if queryset보다 exist가 낫다

But:

##### Don't overuse count() and exist()

queryset의 다른 데이터가 필요하면, 그냥 evaluate 해라. 다음은 optimal한 예시

```python
{% if display_inbox %}
	{% with emails=user.emails.all %} 
      {% if emails %} 
          <p>You have {{ emails|length }} email(s)</p> 
        {% for email in emails %} 
              <p>{{ email.body }}</p>
        {% endfor %} 
        {% else %} 
          <p>No messages today.</p> 
        {% endif %} 
    {% endwith %} 
{% endif %}
```

이는 optimal한데, 

1. QuerySet은 lazy: 'display_inbox'가 False면 db query를 뽑아내지 않음
2. with 사용: user.emails.all을  변수로 사용, 캐시를 허용하여 다시 사용 가능하게 함
3. {% if emails %}은 `Queryset.__bool__()`을 호출하여 user.email.all() 쿼리가 db를 작동시키게 함: 첫 줄로 ORM object가 끝남 (결과가 없으면 False, 있으면 True)
4. {{ emails | length }} 은 `QuerySet.__len__()`을 호출: 다른 쿼리 없이 나머지 캐시를 채움(??)
5. for문은 채워진 캐시로 iterate됨

결과론적으로 이 코드는 한개나 0개의 db 쿼리만을 뽑아낸다: Queryset.exist()나 Queryset.count()를 사용하면 그 시점에 추가적인 쿼리가 실행됨

##### Use QuerySet.update() and delete()

object를 부르고, 변수를 지정하고, 각각을 저장하는 것보다 `QuerySet.update()` 를 사용하여 bulk SQL UPDATE 문을 사용하는 것이 좋다. (bulk delete도 마찬가지)

하지만 bulk update 메소드는 각각의 인스턴스의 save(), delete() 메소드를 부를 수 없기 때문에 추가된 custom behavior를 사용할 수 없다.

##### Use foreign key values directly

만약 foreign key value가 필요하면 전체 오브젝트에서 pk를 가져오기보다 이미 가진 object를 이용하는게 좋다.

```python
# use
entry.blog_id
# instead
entry.blog.id
```

##### Don't order results if you don't care

Ordering은 공짜가 아니다: 각각의 필드의 ordering은 db가 동작한다. 만약 default ordering (Meta.ordering)이 설정되어있는데 이를 사용하지 않으면 파라미터를 지워라. 

##### Insert in bulk

objects를 만들 때 가능하면 *[bulk_create()](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#bulk_createobjs-batch_sizenone-p1165)*를 사용하여 SQL 쿼리문의 수를 줄여라

```python
>>> Entry.objects.bulk_create([ 
... Entry(headline='This is a test'), 
... Entry(headline='This is only a test'), 
... ])
```

다양한 [한계](https://github.com/bartkim0426/django-document/blob/master/models/Queryset%20API%20Reference.markdown#bulk_createobjs-batch_sizenone-p1165)도 있음을 명심. 사용에 적합한 상황인지… 

