## Performing raw SQL queries

django에서는 2가지 방법으로 직접 raw SQL문을 적을 수 있게 한다. (과연 적을일이 있을까 싶지만...)

1. `Manager.raw()`를 사용하여 raw queries를 모델 인스턴스로 사용
2. model layer를 다 avoid 하고 custom SQL을 직접 적기

> raw SQL을 적을 때마다 parameter 사용에 주의해야함. 자세한 내용은 p.506 SQL injection protection



#### Perfoming raw queries

`Manager.raw(raw_query, params=None, translations=None)` 

raw() 메소드는 raw SQL 쿼리를 받아 이를 실행시켜 `django.db.models.query.RawQuerySet` 인스턴스로 반환한다. RawQuerySet 인스턴스는 평범한 QuerySet 과 동일하게 iterate이 가능하다.

```python
class Person(models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    birth_date = models.DateField(...)
```

위의 모델을 예시로 custom SQL문을 만들면

```python
for p in Person.objects.raw('SELECT * FROM myapp_person'):
    print(p)
```

위의 예시는 `Person.objects.all()`과 동일하게 동작한다. 매우 단순해 보이지만 raw()는 다양한 옵션을 통해 강력하게 사용 가능하다.

> **Model table name**
>
> 위 예시의 Person의 테이블명 (myapp_person)은 어디서 나온걸까?
>
> default로 장고는 모델의 "app label" (manage.py startapp에서 사용한 앱 이름)과 "class 이름"을 underscore로 연결하여 테이블명을 만든다.
>
> 디테일한 체크는 db_table 옵션 참고 (p.1121)

> RawQuerySet이 일반적인 쿼리셋과 동일하게 iterate 될 수 있긴 하지만, 몇몇 메소드는 사요이 불가능하다. 
>
> `__bool__(), __len__()`과 같은 메소드는 RawQuerySet에 정의되어 있지 않음 => 모든 RawQuerySet은 True로 된다. 

#### Mapping query fields to model fields

raw()는 자동으로 모델에 있는 필드를 maps(정렬?)한다.

쿼리의 순서는 중요하지 않다. 

```python
>>> Person.objects.raw('SELECT id, first_name, last_name, birth_date FROM myapp_person ˓→') 
...

>>> Person.objects.raw('SELECT last_name, birth_date, first_name, id FROM myapp_person ˓→') 
...
# 위 두 쿼리문은 동일하다

>>> Person.objects.raw('''SELECT first AS first_name, 
... 					  	last AS last_name, 
... 					  	bd AS birth_date, 
... 					  	pk AS id, 
... 					  FROM some_other_table''')
# 위 쿼리문처럼 SQL의 AS문을 사용 가능하다.


>>> name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': ˓→'id'}

>>> Person.objects.raw('SELECT * FROM some_other_table', translations=name_map)
# 다음과 같이 translations를 사용할 수 있다.
```

#### Index lookups

raw()는 인덱싱이 가능하다. 하지만 indexing, slicing은 db level에서는 불가능하기 때문에 db에 많은 정보가 있는 경우에는 SQL level에서 제한을 가하는게 효과적

```python
# 다음과 같이 인덱싱 가능
>>> first_person = Person.objects.raw('SELECT * FROM myapp_person')[0]

# SQL level에서 제한 두기 가능- LIMIT를 사용해서 SQL에서 효율적으로 뽑아냄
>>> first_person = Person.objects.raw('SELECT * FROM myapp_person LIMIT 1')[0]
```

#### Deferring model fields

필드는 필요에 따라서 추출이 가능하다. 

```python
>>> people = Person.objects.raw('SELECT id, first_name FROM myapp_person')

>>> for p in Person.objects.raw('SELECT id, first_name FROM myapp_person'):
    print(p.first_name, # original query에 의해서 retrived됨
          p.last_name) # print문이 돌 때 필요에 의해서 retrived 된다
```

> primary key field는 반드시 raw query에 포함되어야한다. 
>
> 만약 까먹으면 InvalidQuery exception이 발생

#### Adding annotations

```python
>>> people = Person.objects.raw('SELECT * , age(birth_date) AS age FROM myapp_person')

>>> for p in people:
... print("%s is %s." % (p.first_name, p.age))
John is 37.
Jane is 42.
...
```

model에 define되지 않은 필드도 포함시킬 수 있다. 위의 예시는 PostgreSQL의 age() 기능을 이용한것이다.

#### Passing parameters into raw()

raw()에 params argment를 사용하여 파라미터 쿼리를 구현하 수 있다.

```python
>>> lname = 'Doe'
>>> Person.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', [lname])
```

params는 리스트나 dict 파라미터를 이용한다. 

> SQLite backend에서는 list 파라미터만 사용 가능하다

> raw query에서 string formatting을 사용하지 말아라: [SQL injection attack](https://en.wikipedia.org/wiki/SQL_injection)의 원인이 될 수 있다.
>
> ```python
> >>> query = 'SELECT * FROM myapp_person WHERE last_name = %s' % lname
> >>> Person.objects.raw(query)
> ```
>
> 위의 예시와 같이 사용하면 안된다. parameter를 사용해서 raw query 만들기

#### Executing custom SQL directly (p.143)

Manager.raw()가 충분하지 않은 경우 database에 직접 access 가능하다.

`django.db.conntection`오브젝트는 default dabatase connection

`connection.cursor()`를 사용해 cursor object를 불르고 `cursor.execute(sql, [params])`을 통해 SQL문을 실행시키고 `cursor.fetchone()`, 혹은 `cursor.fetchall()`을 통해 결과 rows를 반환

```python
from django.db import connection 

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz]) 
        row = cursor.fetchone()
        
    return row
```

여려 개의 db를 사용하는 경우 `django.db.connections`를 사용하여 특정 데이터베이스를 선택할 수 있다.  dict 형태의 오브젝트.

```Python
from django.db import connections
cursor = connections['my_db_alias'].cursor() # 이렇게 특정 db 선택
```

기본적으로 파이썬 DB API는 결과물을 필드명 없이 반환, list value가 나온다. 메모리 코스트를 줄이기 위해 dict 형태의 결과물을 만들어낼 수 있다.

```python
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
      	dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
```

다른 옵션은 `collections.namedtuple()`를 사용 가능하다. namedtuple은 속성 lookup으로 접근이 가능하고, immutable한 tuple-like 객체이다.

```python
from collections import namedtuple

def namedtuplefetchall(cursor):
	desc = cursor.description
	nt_result = namedtuple('Result', [col[0] for col in desc])
	return [nt_result(*row) for row in cursor.fetchall()]
```

위 예시들의 결과 차이는 document 참고 (p.144)

#### Connections and cursors

Connection, cursor는 [PEP 249](https://www.python.org/dev/peps/pep-0249/)의 Pyhon DB-API에 기반한 도구이다. (transcation handling만 빼고)

cursor.execute() 의 SQL statement는 SQL에 직접 paramete를 추가하기보다는 "%s" placeholder를 사용한다. s