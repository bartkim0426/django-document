## Manager (p.132~)

class Manager

Manager is the interface through which database query operations are provided

모든 모델은 적어도 한개의 매니저를 가짐

### Manager names

default로 장고는 `objects`라는 이름의 Manager를 추가해준다

=> 필드명으로 objects를 사용하거나, 다른 이름을 사용하고 싶으면 rename이 가능하다. 

```python
from django.db import models


class Person(models.Model):
    # ...
    people = models.Manager()
```

위처럼 people이 기존의 objects를 대체해서 쓰임. 이렇게 되면 Person.objects는 AttributeError가 발생

### Custom managers

기본 base Manager을 extending해서 커스텀 Manager를 사용 가능하다. 

=> 두가지 이유로 커스텀

1. 추가적인 Manager 메소드 사용을 위해서
2. Manager가 리턴하는 기본 QuerySet의 수정을 위해서

### Adding extra manger methods (p.133)

메소드를 추가 할 때에는 모델에 "talbe-level" 기능을 추가하는 것이 낫다. 

(모델 오브젝트의 single instance를 추가하거나 할 때는 "row-level" 기능을 사용- Model methods를 사용, custom Manager를 사용하지 말고...)

Custom Manager는 QuerySet 말고도 어떤 것도 리턴이 가능하다. 

ex) OpinionPoll object의 리스트를 반환하는 with_counts() 메소드를 추가

```python
from django.db import models

class PollManager(models.Manager):
    def with_counts(self):
        from django.db import connection 
        with connection.cursor() as cursor:
            cursor.execute(""" SELECT p.id, p.question, p.poll_date, COUNT( * )
            FROM polls_opinionpoll p, polls_response r 
            WHERE p.id = r.poll_id 
            GROUP BY p.id, p.question, p.poll_date O
            RDER BY p.poll_date DESC""")
            
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], question=row[1], poll_date=row[2]) 					p.num_responses = row[3] 
                result_list.append(p)
        return result_list
```

### Modifying a manger's initial QuerySet (p.134)

매니저의 기본 쿼리셋은 시스템의 모든 객체를 반환함 `Book.objects.all()`처럼...

이 기본 쿼리셋을 오버라이딩 가능 => `Manager.get_queryset()` 메소드로 

아래 예시는 Roald Dahl의 책만을 뽑아내는 매니저를 만든다

```python
class DahlBookManager(models.Manager):
    def get_queryset(self):
        return super(DahlBookManager, self).get_queryset().filte(author='Roald Dahl')
    
    
class Book(models.Manager):
    title = models.CharField(max_lenght=100)
    author = models.CharField(max_length=50)
    
    objects = models.Manager()
    dahl_objects = DahlBookManager()
```

=> 이제 `Book.objects.all()` 이외에도 `Book.dahl_objects.all()`로 달이 쓴 책들만 뽑아낼 수 있다. 

위 예시에서 볼 수 있듯이 한 모델에 여러 매니저를 사용 가능하다. 

#### Default managers (p.135)

`Model._default_manager`

custom Manager를 만들면 장고의 기본 매니저는 특별한 상태가 된다: 'default' 상태가 되서 장고가 가진 몇몇 기능들은 오직 이 기본 매니저로만 사용할 수 있다 (dumpdata 등…) 

Meta.default_manager_name을 통해서 이 매니저를 커스텀할 수 있다. 

#### Base managers

`Model._base_manager`

#### Using managers for related object access

related objects(ex. choice.question)에 대해서 장고는 Model._base_manager 인스턴스를 사용해 접근한다. 

#### Don't filter away any results in this type of manager subclass

base manager는 다른 모델과 관련된 모든 objects들에 접근이 가능한데, get_gueryset() 메소드를 오버라이드하면 잘못된 결과를 리턴한다. get_queryset()은 base manager에 맞지 않으니 사용하지 말아라

#### Calling custom QuerySet methods from the manager

```python
class PersonQuerySet(models.QuerySet):
    def authors(self):
        return self.filter(role='A')
	
    def editors(self):
        return self.filter(role='E')

class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)
	
    def authors(self):
        return self.get_queryset().authors()
	
    def editors(self):
        return self.get_queryset().editors()

class Person(models.Model):
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    role = models.CharField(max_length=1, choices=(('A', _('Author')), ('E', _('Editor ˓→')))) 
    people = PersonManager()
```

위 예시에서처럼 Person.people 매니저로 authors(), editors()를 바로 부를 수 있다.

#### Creating a manager with QuerySet methods

위의 방법들은 QuerySet, Manager의 메소드가 모두 필요하다.

`Queryset.as_manager()`는 custom QuerySet의 메소드의 카피와 함께 매니저의 instance를 만들어준다.

```python
class Person(models.Model):
    ...
    people = PersonQuerySet.as_manager()
```

#### from_queryset()

custom Manager, custom QuerySet을 동시에 사용할 경우 `Manager.from_queryset()`을 사용 가능하다.

```python
class BaseManager(models.Manager):
    def manager_only_method(self):
        return

class CustomQuerySet(models.QuerySet):
    def manager_and_queryset_method(self):
        return

class MyModel(models.Model):
    objects = BaseManager.from_queryset(CustomQuerySet)()
```

#### Custom managers and model inheritance

장고가 cusom managers, model inheritance를 다루는 방법

1. base class의 매니저는 child class에 상속된다.
2. parent class에서 매니저가 선언되지 않았으면 장고는 자동으로 objects manager를 생성
3. default 매니저는: Meta.default_manager_name으로 선택된 매니저 / 처음으로 선언된 매니저 / parent model에서의 default 매니저

abstract base class를 통해서 custom manager를 여러 모델에 적용시킬 수 있다.

```python
class AbstractBase(models.Model):
    ...
    objects = CustomManager()
    
    class Meta:
        abstract = True
```

```python
class ChildA(AbstractBase):
#     위의 AbstractBase를 상속받으면 child class의 default manager는 objects가 된다. 
    pass


class ChildB(AbstractBase):
    default_manager = OtherManager()
	# default 매니저를 따로 선언해서 사용할 수 있다.
    # 상속받은 objects 또한 사용 가능
```

위처럼 추가할 수 있지만 default를 AbstractBase에서 사용하고 싶다면 다른 abstract class를 상속받으면 된다.

```python
class ExtraManager(models.Model):
    extra_manager = OtherManager()
    
    class Meta:
        abstract = True
        
class ChildC(AbstractBase, ExtraManager):
    pass
```

위의 예시에서 default manager는 상속받은 objects이지만 별개로 extra_manager 또한 사용이 가능하다.





