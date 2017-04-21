## Multiple database (p.153~)

대부분의 장고 공식 문서는 single db을 가정한 것이다. 만약 여러 db를 사용하려면 몇몇 추가적인 설정을 해야한다. 

#### Defining your database

여러 db를 사용하는 첫 단계: 장고에게 어떤 db server를 사용하는지 알려주는 것! 

DATABASE setting이 필요하다. (p.1235 참고)

다음은 PostgreSQL, MySQL db를 사용한 예이다

```python
DATABASES = {
	'default': { 
        'NAME': 'app_data', 
        'ENGINE': 'django.db.backends.postgresql', 
        'USER': 'postgres_user', 
        'PASSWORD': 's3krit' 
    }, 
    'users': { 
        'NAME': 'user_data', 
        'ENGINE': 'django.db.backends.mysql', 
        'USER': 'mysql_user', 
        'PASSWORD': 'priv4te' 
    }
}
```

장고는 default db를 필요로 하지만, 사용하지 않을 거라면 그냥 빈 dict로 놓아도 괜찮다. 이를 위해서는 앱들(모든 contrib, third-party apps)의 모델에서 DATABASE_ROUTERS(p.1241)를 설정해줘야한다. 

만약 DATABASE settings이 되지 않은 상태에서 db에 접근하려고 하면 `django.db.utils.ConnectionDoesNotExist`  예외가 발생한다.

#### Synchronizing your database: DB 싱크로나이즈 하기

`migrate`(p.989) 명령어는 한 번에 하나의 db에만 작동된다. default로는 default db에 작동하는데, -\-database 옵션을 주어서 다른 db에 synchronize 할 수 있다.

`$ ./maage.py migrate —database=users`

#### Using other management commands

db에 작용하는 다른 대부분의 django-admin 코맨드들도 migrate와 비슷한 방식으로 작동한다: —database을 통해 db를 선택 가능하다.

Makemigrations 커맨드에만 예외 => 존재하는 migration 파일들의 db history의 문제를 validate: default db만을 체크. routers의 `allow_migrate()` 메소드로 체크 가능

#### Automatic databae routing

여러 db를 사용하는 가장 쉬운 방법: database routing scheme를 설정하는 것.

기본 routing scheme는 오리지널 db와 오브젝트가 sticky하게 유지되게 도와준다 (?) defatult routing scheme는 모든 장고 프로젝트에 제공되기 때문에 따로 activate 할 필요는 없지만 더 많은 db allocation behavior을 위해서 자신만의 db router를 설치 가능하다.

#### Databae routers (p.155)

db Router는 다음 4가지의 메소드를 제공하는 class이다. 각각의 자세한 설명은 document

**db_for_read**(*model, \*\*hints*)

**db_for_write**(*model, \*\*hints*)

**allow_relation**(*obj1, obj2, \*\*hins*)

**allow_migrate**(*db, app_label, model_name=None, \*\*hints*)

**Hints** 

#### Using routers

Database routers는 DATABASE_ROUTERS setting에 설치된다. 이 세팅은 class name의 리스트로 되어있고 각각은 master router를 사용해야한다 (django.db.router)

#### An example (p.156-159)

=> multiple db를 쓰실 분들은 example을 한번 쭉 따라해 보시면 좋을 것 같습니다.

> DATABASE_ROUTERS의 순서가 중요: default가 없고, db 선택시 따로 지정하지 않았다면 DATABASE_RUTERS 리스트에 가장 먼저 있는 db를 선택함.

#### Manually selecting a database

수동으로 db를 선택하면 router의 순서보다 더 먼저 적용된다.

##### Manually selecting db for a QuerySet: 쿼리문에서 db 선택

 QuerySet chain의 어느 포인트에서나 db를 선택 가능하다. `using()`을 사용하여…

```python
# 'default' db를 불러온다.
>>> Author.objects.all()

# 이것도 위와 마찬가지로 default를 부른다
>>> Author.objects.using('default').all()

# 이는 'other' db를 사용
>>> Author.objects.using('other').all()
```

##### Selecting a databae for save(): save() 메소드에서 db 선택

`using()`은 Model.save() 에서도 사용이 가능하다.

```python
# legacy_users 데이터베이스에 object를 저장
>>> my_object.save(using='legacy_users')
```

##### Moving an object from one db to another: 다른 db로 object 옮기기

save(using=…)를 활용해서 각각의 db에 두 번 저장해줘야한다.

```python
>>> p = Person(name='Fred')
>>> P.save(using='first')
>>> p.save(using='second')
```

첫 번째 p.save(using='first')에서 p에 primary key가 생기고, 이미 가지고 있는 pk를 second db에 저장할 때 똑같이 적용이 된다. 두 번 째 db ('second')에 해당 pk가 없다면 문제가 안 되지만 있다면 object가 overriding 되는 문제가 발생할 수 있다. 

=> 두가지 방법으로 해결 가능

1. 저장 전에 instance가 가지고 있는 pk를 초기화

```python
>>> p = Person(name='Fred')
>>> P.save(using='first')
>>> p.pk = None # primary key를 초기화
>>> p.save(using='second')
```

2. save() 메소드에 `force_insert`를 추가

```python
>>> p = Person(name='Fred')
>>> P.save(using='first')
>>> p.save(using='second', force_insert=True)
```

`force_insert=True`가 있다면 만약 동일한 pk가 'second' db에 있을 때 에러가 발생하게 된다.

##### Selecting a db to delete from

default로 `delete()` 를 사용하면 이전에 선택된 db와 동일한 db가 적용이 된다.

```python
>>> u = User.objects.using('legacy_users').get(username='fred')
>>> u.delete() # 'legacy_users의 db에 있는 값을 지운다.
```

이를 구체화 하려면 save()와 마찬가지로 using()을 사용해 주면 된다.



#### Using managers with multiple databases (p.161)

`db_manager()` 메소드를 사용하면 manager가 non-default db에 접근할 수 있다.

ex) `User.objects.create_user()` 를 예로 들어보면, create_user()는 오직 User.objects에서만 접근 할 수 있기 때문에 `User.objects.using('new_users').create_user()`와 같은 방식으로는 부를 수 없다. 이를 해결하기 위해서 db_manager()를 사용 가능하다.

```python
User.objects.db_manager('new_users').create_user(...)
```

#### Using get_queryset() with multiple db

```python
class MyManager(models.Manager):
    def get_queryset(self):
        qs = CustomQuerySet(self.model) 
        if self._db is not None:
            qs = qs.using(self._db) 
        return qs
```

#### Exposing multiple db in django's admin interface

장고 admin에서는 따로 multiple db를 지원하지 않아 custom ModelAdmin class를 만들어야한다.

ModelAdmin objects는 5개 메소드를 customize 해야한다. 

```python
class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database. using = 'other'
    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

	def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

	def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

	def formfield_for_foreignkey(self, db_field, request, ** kwargs):
        # Tell Django to populate ForeignKey widgets using a query 
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, ˓→request, using=self.using, ** kwargs)

	def formfield_for_manytomany(self, db_field, request, ** kwargs):
        # Tell Django to populate ManyToMany widgets using a query 
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, ˓→request, using=self.using, ** kwargs)
```

위의 예시에 있는 5개의 메소드를 커스터마이징 해야한다. 더 더 복잡하게 하려면 super()를 이용해서 다양하게 어렵게 해야한다… p.162 를 참고

#### Using raw cursors with multiple db

`django.db.connections`으로 불러온 connection에 dict 형태로 특정 db를 지정 가능하다.

```python
from django.db import connections
cursor = connections['my_db_alias'].cursor()
```

#### Limitations of multiple database

##### Cross-database relations

현재로서 장고는 foreign key, many-to-many relationshipo에 대한 여러개의 db 사용 지원이 전혀 없다. 여러 db를 사용하더라도 foreingn key, many-to-many 관계는 반드시 하나의 db에 정의되어야함.

##### Behavior of contrib apps

Models 등 몇몇 contrib 앱들은 다른 것들에 의존적이다. cross-db relationship이 불가능하기 때문에 모델을 db에 나누는 것에는 몇몇 제한들이 존재한다.

- auth: User, Group, Permission: 같은 db에 저장되어야함
- admin: auth에 의존적 - auth와 같은 db에 저장
- Flatpages, redirects: sites에 의존적- site와 같은 db에 저장