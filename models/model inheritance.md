## model inheritance

### Model inheritance (p.96)

모델을 실제로 만들어서 가질지, 아니면 info로 가지게 할지를 결정해야함

(parent models to be models in their own right / just holders of common information )

상속에 3가지 스타일이 있다.

1. parent class를 사용: child model이 가지지 않았으면 하는 정보를 가지게. 

> 이 클래스는 isolation일 필요 없음 => Abstract base classes 사용

2. (아마 다른 어플리케이션에 있는) 존재하는 모델의 subclassing, 각각의 모델이 각각의  db 테이블을 갖게 할 경우
3. ​

> Multi-table inheritance를 사용

3. 모델 필드의 변화 없이 'Python-level behavior'을 수정하고 싶으면..  Python-level이 뭘 말하는거지?

> Proxy models



#### 1. Abstract base classes

common information을 다른 모델들로 옮기고 싶을 때 유용.

base 클래스에 `abstract=True`를 Meta class에 넣어줌 => 이 모델은 더이상 db 테이블을 생성하지 않는다. 

대신 다른 모델의 base class로 사용된다. => child class에 추가됨,

> 만약 child와 class name이 같으면 에러 발생

예시

```python
from django.db import models 

class CommonInfo(models.Model):
    name = models.CharField(max_length=100) 
    age = models.PositiveIntegerField()

	class Meta:
        abstract = True 
       
class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```

Student 클래스는 name, age, home_group을 가짐. 

##### Meta inheritance

child 클래스에서 Meta를 따로 지정하지 않으면 parent의 Meta를 상속. extend도 가능하다.

```python
from django.db import models 

class CommonInfo(models.Model):
	# ...
	class Meta:
		abstract = True 
        ordering = ['name'] 
        
class Student(CommonInfo):
    # ...
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'
```

Meta attribute를 상속 받기 전에 `abstract=False`가 적용됨. 상속받을 클래스에서 `abstract=True`를 매번 적용해줘야한다. (db_table과 같은 값들은 상속받으면 안됨. Child class마다 다를거기 때문에)



##### be careful with related_name, related_query_name

ForeignKey, ManyToManyField에서 related_name, related_query_name을 사용할 때에 앱이 다른데 클래스 명이 똑같은 상황을 피하기 위해서 

`%(app_label)s`: lower-cased name of app

 `%(class)s`: lower-cased name of child class

를 꼭 넣어줘야한다.

```python
from django.db import models 

class Base(models.Model):
	m2m = models.ManyToManyField( 
        OtherModel, 
        related_name="%(app_label)s_%(class)s_related", 
        related_query_name="%(app_label)s_%(class)ss", 
    )

	class Meta:
        abstract = True
```

`common/models.py`의 ChildA m2m 클래스는

`common_childa_related`, `common_childas`

로 다른 클래스들과 다른걸 알 수 있다. 

(쓰지 않으면 migrate할때 에러 발생)

> 만약 related_name을 abstract base class에 주지 않으면 자동으로 '_set'으로 생성된다. 



### 2. Multi-table inheritance

두 번째 모델 상속 방법은 각각의 모델을 갖는것.

자동으로 생성되는 OneToOneField를 통해서 연결된다. 

```python
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50) 
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False) 
    serves_pizza = models.BooleanField(default=False)
```

위 예시에서 Place의 모든 필드들은 Restaurant에서 사용 가능. (데이터는 각각의 테이블에 저장됨)

##### Meta and multi-table inheritance

Child model에서 parentmodel의 meta 옵션을 상속받는게 말이 안된다? (이미 parent class에서 적용되었기 때문에 다시 적용되지 않는다?) access 할 수 없다는 말. 

하지만 명시적으로 disable 할 수는 있다.

##### Inheritance and reverse relations (p.99)

이해가 잘 안됨.

ForeignKey, ManyToManyField 관계에서 상속을 받으면 related_name 속성을 꼭 넣어줘야함 (안그러면 에러 발생)

예시

```python
class Supplier(Place):
    customers = models.ManyToManyField(Place, related_name='provider')
```

##### Specifying the parend link field

OneToOneField 링크를 장고에서 자동으로 만들어주지만, `parent_link=True`를 통해 직접 만들 수 있음



### 3. Proxy models

단순히 Python behavior을 수정하거나 default manager 변경, method 추가만 필요할 때 사용

proxy model을 만들어 이를 오리지널 모델에 저장 할 수 있다.  

(살짝만 바꾼다는게...)

