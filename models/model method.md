## Model methods

p.94

직접 모델 메소드를 만들 수 있다.

ex)

```python
from django.db import models

class Person(models.Model):

	first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    birth_date = models.DateField()

    def baby_boomer_status(self):
    "Returns the person's baby-boomer status." 
		import datetime 
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer" 
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer" 
        else:
            return "Post-boomer"

	def _get_full_name(self):
    "Returns the person's full name."
    	return '%s %s' % (self.first_name, self.last_name) 
    full_name = property(_get_full_name)
```

### Overriding predefined model method (p.95)

save(), delete() 등의 메소드를 오버라이딩 할 수 있다. 

```python
from django.db import models 

class Blog(models.Model):
	name = models.CharField(max_length=100) 
    tagline = models.TextField()

	def save(self, * args, ** kwargs):
		do_something() 
        super(Blog, self).save( * args, ** kwargs) # Call the "real" save() method. 
        do_something_else()
```



p.1135~

### Other model instance methods

#### `__str__()`

`Model.__str__()`

오브젝트의 str()을 사용할 때 불러지는 메소드.  어드민 사이트나 템플릿에서 보여질 때 등 다양하게 사용된다. 그래서 nice, human-readable한 방식으로 직접 해주는 것이 좋다. 모든 모델에 쓸것!

### `__eq__()`

The equality method is deﬁned such that instances with the same primary key value and the same concrete class are considered equal, except that instances with a primary key value of None aren’t equal to anything except themselves. For proxy models, concrete class is deﬁned as the model’s ﬁrst non-proxy parent; for all other models it’s simply the model’s class.

=> 무슨 말인지 잘 모르겠다… Q)

#### `__hash__()`

instance의 primary key value에 기반(?) ???



### get_absolute_url()

어떻게 표준 URL을 계산하는지 지정해주는 메소드. 

```python
def get_absolute_url(self):
	return "/people/%i/" % self.id
```

맞고 간편한 예시이지만, 좋은 방법이 아니다. (하드 코딩이기 때문에, 템플릿에서 이런식으로 하드 코딩으로 부르는건 좋지 않다. `{{ object.get_absolute_url }}`로 쓰는게 맞는 방법) reverse() function이 주로 쓰인다. 다음처럼...

```python
def get_absolute_url(self):
	from django.urls import reverse 
    return reverse('people.views.details', args=[str(self.id)])
```



### Extra instance methods

save(), delete() 이외에도 다음의 다양한 메소드들을 사용 가능하다.

#### get_FOO_display()

Choices set이 있는 모든 필드가 가질 수 있다. FOO 대신 field name을 입력해주면 됨. 'human-readable' value (튜플에서 두번째 값)을 리턴해준다.

```python
from django.db import models 

class Person(models.Model):
	SHIRT_SIZES = ( ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ) 
    name = models.CharField(max_length=60) 
    shirt_size = models.CharField(max_length=2, choices=SHIRT_SIZES)
```

위의 예시 모델에서

```python
>>> p = Person(name="Jack", shirt_size="L")
>>> p.save()
>>> p.shirt_size # "L" (db의 값)이 리턴된다.
'L'
>>> p.get_shirt_size_display() # human-readable value가 리턴된다.
'Large'
```

#### get_next_by_FOO(\*\*kwargs), get_previous_by_FOO(\*\*kwargs)

null=True 값을 갖지 않은 DateField, DateTimeField는 이 메소드들을 갖는다. (FOO는 필드명)

date field에 기반한 전/후의 오브젝트를 호출해준다.