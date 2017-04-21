## Querys



### Making querys

아래 예시를 통해 query 문을 다루는 법을 설명

```python
from django.db import models 

class Blog(models.Model):
    name = models.CharField(max_length=100) 
    tagline = models.TextField()
    
    def __str__(self):
        return self.name 
    

class Author(models.Model):
    name = models.CharField(max_length=200) 
    email = models.EmailField() 
    
    def __str__(self): # __unicode__ on Python 2 
        return self.name 
    
    
class Entry(models.Model):
    blog = models.ForeignKey(Blog) 
    headline = models.CharField(max_length=255) 
    body_text = models.TextField() 
    pub_date = models.DateField() 
    mod_date = models.DateField() 
    authors = models.ManyToManyField(Author) 
    n_comments = models.IntegerField() 
    n_pingbacks = models.IntegerField() 
    rating = models.IntegerField()

	def __str__(self):
        return self.headline
```

#### Creating objects

```python
>>> from blog.models import Blog
b = blog(name='Blog', tagline='All of blog')
b.save()
```

save() 메소드를 호출 할 때까지는 데이터베이스에 저장되지 않는다.

create()를 쓰면 create/save가 포함됨

#### Saving changes to objects

Update 할 때에도 save()를 호출하면 SQL의 UPDATE와 같은 기능을 함

#### Saving ForeignKey and ManyToManyField fields

ForeignKey에서는 똑같은 방식으로 저장됨. 

ManyToManyField에서는 조금 다름 -> add() 메소드를 사용

```python
from blog.models import Author, Entry, Blog
entry = Entry.objects.get(pk=1)
my_blog = Blog.objects.get(name="my blog")
entry.blog = my_blog # 바로 이렇게 가능
entry.save()
joe = Author.objects.create(name='Joe')
entry.authors.add(joe) # ManyToMany 필드에서는 add()를 사용
john = Author.objects.create(name='Jhon')
paul = Author.objects.create(name='Paul')
entry.authors.add(johin, paul) # 여러 argument를 한번에 추가 가능
```

#### Retrieving objects (p.106)

매니저를 통해 queryset을 형성 가능하다. default로 `objects`로 불러짐 (매니저가)

> QurerySet: collections of objects from your db, 0개부터 여러개 필터 가능. SELECT와 비슷한 기능

매니저는 model 클래스로만 접근 가능하고 모델 인스턴스로 호출하려고 하면 오류가 발생함

#### Retrieving all objects

모든 오브젝트를 선택하려면 `all()`로 선택 

#### Retrieving specific objects with filters

`filter`와 `exclude`를 통해서 특정 컨디션의 쿼리셋을 선택 가능하다.

Filter: 여러 개의 필터를 한번에 선택 가능, 각각의 쿼리셋은 독립적. 

다양한 쿼리셋은 따로 Field lookups에 정리 (p109)

#### Querysets are lazy

쿼리셋은 evaluated 될 때까지 database에 영향을 미치지 않음

itration, slicing, pickling, repr(), len(), list(), bool(): When QuerySets are evaluated(p.1139)에 자세하게 설명됨 

#### Retrieving a single object with get()

filter()는 하나의 오브젝트만 매칭되도 쿼리셋이 반환된다. 한 개의 object만 선택할 때 get()을 사용하면 됨

> 만약 값이 없으면 DoesNotExist, 값이 여러개면 MultipleObjectsReturned 에러를 발생
>
> filter()[0]은 에러 발생 X

#### Other QuerySet methods

all(), get(), filter(), exlude() 이외에도 여러 메소드 - QuerySet API Reference (p.1141) 참고. 따로 정리함.

#### Limiting QuerySets

python의 array-slicing syntax를 사용 가능

```python
>>> Entry.objects.wall()[:5]
>>> Entry.objects.all()[5:10]
>>> Entry.objects.all()[:10:2]
```

[-1]은 지원되지 않는다. reverse()로 사용하면 됨



### Fields lookups

p.109

filter(), exclude(), get()에서 SQL의 WHERE처럼 사용 가능. Field__lookuptype=value 와 같이 사용 (더블스코어)

p.1171에 목록들은 따로 정리



#### lookups that span relationships

lookups을 연결시켜서 사용 가능하다. 

```python
Blog.objects.filter(entry__authors__name='Lennon')
Blog.objects.filter(entry__authors__isnull=False, entry__authors__name__isnull=True)
```

#### Spanning multi-valued relations

```python
Blog.objects.filter(
	entry__headline__contains='Lennon',
    entry__pub_date__year=2008,
)
```

#### Filters can reference fields on the model

지금까지는 모델 필드의 값들끼리만 비교. 같은 모델의 다른 필드랑 비교하려면? 

장고에서는 'F expressions' 제공: 