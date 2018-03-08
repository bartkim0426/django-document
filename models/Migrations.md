## Migrations



### The commands (p.304)

- #### migrate: 실제로 적용/ 비적용

- makemigrations: 변경된 모델을 바탕으로 새로운 migrations를 만듬

- sqlmigrate: migration의 SQL문을 보여줌

- showmigrations: 프로젝트의 migrations와 상태를 보여줌

Migrations을 db schema의 버전관리 시스테ㅐㅁ으로 생각하면 됨: migrations file은 commit과 비슷하고 migrate는 실제 데이터에 적용

각각의 앱 디렉토리 안에 "migration" 폴더에 Migrations 파일들이 있다. 

장고는 모델 필드의 모든 변화를 migrations으로 만든다 (db에 영향을 미치지 않는 상황에도)





### Backend Support

다양한 써드파티 백엔드를 지원하고 필요할 경우 schema alteration(변경?)도 지원함 - [schemaEditor]()(p.1226, the database abstraction layer that turns things like “create a model” or “delete a ﬁeld” into SQL - which is the job of the SchemaEditor.)활용 가능

#### PostgreSQL

schema support 중에 가장 capable한 db: 유일한 caveat(경고?)는 default values를 가진 칼럼을 만들때 전체 테이블을 다시 rewrite하여 이에 비례하는 시간이 걸림. => 그래서 null=True로 칼럼을 만드는걸 추천: 바로 추가된다

>   django에서 일반모델은 blank=True, ForeignKey가 적용된 모델은 null=True, blank=True

#### MySQL

MySQL은 schema alteration operation의 트랜젝션 지원이 떨어짐: migration이 실패했을 경우 그냥 다시 시도하면 안되고 변화된걸 수동으로 unpick해야함.. (다시 롤백하기 불가능)

추가적으로 MySQL은 거의 모든 작업에서 테이블을 rewrite하기 때문에 시간이 오래걸림. 느린 하드웨어에서는 몇개의 칼럼을 테이블에 추가하다가 사이트가 10분넘게 뻑날수도 있다 (!)

마지막으로 MySQL은 칼럼, 테이블, 인덱스의 길이에 상대적으로 적게 제한: 다른데서는 되는 index들이 MySQL에서 실패할수도있따.

#### SQLite

SQLite는 아주 작은 빌트인 schema alteration support. 

장고는 emulate하려고 시도한다=>(모방한다?)

- createing new table with new scheme
- copying data across
- dropping old table
- renaming new table to match original name

이 프로세스는 잘 되긴 하지만 느리고 buggy함. 프로덕션 레벨에서 SQLite 쓰는거 비추. 로컬에서 사용하길





### Workflow 

simple: 모델을 변경 (필드 추가/제거) => [makemigrations]()(p.988) 실행

```python
$ python manage.py makemigrations 
Migrations for 'books':
books/migrations/0003_auto.py:
- Alter field author on book
```

=> 모델은 최근 마이그레이션 파일을 스캔하고 비교해서 새로운 마이그레이션 셋을 만들어줌. => 결과물이 정확히 원하는거랑 일치하는지 확인 필요 (완벽하지 않기 때문에 복잡한 변화를 detect 못할수도 있따.)

migrations 파일이 생기면, 이를 db에 적용시켜야함

```python
$ python manage.py migrate 
Operations to perform:
Apply all migrations: books 
Running migrations:
Rendering model states... DONE
Applying books.0003_auto... OK
```

migration이 적용되면, 버전관리 툴에서 single commit을 날려라: 다른 개발자 (production servers)가 코드를 체크하고 모델을 변경해서 migration을 같은 시간에 할 수 있도록… (이런방법밖에 없나)

migration(s)에 이름을 붙이고 싶으면 makemigrations —name 옵션 사용 가능 (더 많은 명령어는 988p 참조 - 따로정리)

#### Makemigrations 명령어 (p.988)

**django-admin makemigrations [app_label [app_label …]]**

Creates new migrations based on the changes detected to your models. Migrations, their relationship with apps and more are covered in depth in the migrations documentation.

Providing one or more app names as arguments will limit the migrations created to the app(s) speciﬁed and any dependencies needed (the table at the other end of a ForeignKey, for example).

**--noinput, --no-input**

 Suppresses all user prompts. If a suppressed prompt cannot be resolved automatically, the command will exit with error code 3.

The --no-input alias was added.

**--empty **

Outputs an empty migration for the speciﬁed apps, for manual editing. This is for advanced users and should not be used unless you are familiar with the migration format, migration operations, and the dependencies between your migrations.

**--dry-run **

Shows what migrations would be made without actually writing any migrations ﬁles to disk. Using this option along with --verbosity 3 will also show the complete migrations ﬁles that would be written.

**--merge **

Enables ﬁxing of migration conﬂicts.

**--name **

NAME, -n NAME Allows naming the generated migration(s) instead of using a generated name.

**--exit, -e**

Deprecated since version 1.10: Use the --check option instead.

Makes makemigrations exit with error code 1 when no migrations are created (or would have been created, if combined with --dry-run).

**--check **

Makes makemigrations exit with a non-zero status when model changes without migrations are detected.



#### Version control (p.306)

migrations는 버전 컨트롤에 저장되므로 다른 개발자가 동시에 같은 앱에 migration을 코밋하는 상황이 발생: 같은 숫자를 가진 두개의 migrations 파일이 존재.

"Dont't worry"- 숫자는 개발자의 레퍼런스일 뿐, 장고는 각각의 migration을 다른 이름으로 인식. (오)

(Migrations specify which other migrations they depend on - including earlier migrations in the same app - in the ﬁle, so it’s possible to detect when there’s two new migrations for the same app that aren’t ordered.)  => 여하튼 두개의 새로운 마이그레이션을 인식하는게 가능

이런일이 발생했을때 장고는 option 제공: 안전하다고 생각하면 자동으로 두 migrations을 linearize (선형?), 아니라면 직접 수정. (don't worry, this isn't difficult ㅋㅋ 아래 나오는[Migration files]()()참고)





### Dependencies

migrations은 앱단위기: 모든 앱을 한번에 migrate 하면 모델에서 언급하는 table, relationship들이 너무 복잡. 다른게 필요한 migration을 할 수도

(ex: books app에 ForeignKey로 authors app이 물려있으면 migration의 결과는 authors의 migration에 depenency를 가짐)

==> migrations을 진행하면 `authors` 의 migration이 먼저 진행되어 ForeignKey 레퍼런스를 가진 table을 만들고 ForeignKey 컬럼을 그 다음에 사용. 

이렇게 되지 않으면 없는 table에서 ForeinKey를 가져오려고 하기 때문에 에러...

(makemigrations, migrate 모두) single app으로 제한하는 것: best-efforts promise, and not a guarantee;





### Migration files 

migrations는 on-disk 포멧으로 저장됨. 이 파일들은 사실 평범한 파이썬 파일 (with an agreed-upon object layout, written in a declarative style.)

기본적인 migration 파일은 다음처럼 생겼다:

```python
from django.db import migrations, models 


class Migration(migrations.Migration):
	dependencies = [("migrations", "0001_initial")]

	operations = [ migrations.DeleteModel("Tribble"), 
    	migrations.AddField("Author", "rating", models.IntegerField(default=0)), 
    ]
```

마이그레이션 파일 (파이썬 모듈)에서 장고는 `django.db.migrations.Migration`을 부름: object의 4가지 속성을 검사 (대부분의 경우에는 두가지만 쓰인다)함

- *dependencies*: 마이그레이션이 의존하는 리스트
- *operations*: 마이그레이션이 하는 것을 정의하는 Operation 클래스의 리스트

operations은 key: 장고에게 만들어질 schema 변화를 알려줌. 장고는 이를 스캔하여 모든 앱의 스케마 변화를 적용한 in-memory representration을 만들고, 이를 이용하여 SQL을 생성

이 in-memory 구조는 현재 상태와 모델간의 변화를 알려주는데도 사용: in-memoy 모델과 최근 makemigrations 한 상태의 모델의 변화를 인식 => 이후 이 모델을 사용하여 models.py 파일과 비교하고, 변화된 상태를 파악 (??)

아주 가끔 (해야한다면) 이 migration file을 직접 수정해야 할수도 있따: 전체를 직접 적는것도 필요하다면 가능. 몇몇 더 복잡한 작업들은 자동으로 탐지될 수 없고 직접 쓸 수 밖에 없기 때문에 => 직접 적는걸 두려워하지 말아라(!)

#### custom fields

이미 migrate 된 커스텀 필드의 positional argument의 숫자를 수정할 수는 없음.

이전 migration은 `__init__` 메소드를 사용하여 수정 가능. 새로운 argument가 필요하다면 keyword argumenyt를 만들고 constructor에 assert 'argument_name'을 추가해라 …(??)

#### Model managers

migrations에 managers를 serialize 할수있음: [RunPython operations]()(p.1084- historical context에서 Custom Python code 실행 가능)로 가능.

자세한 내용은 [Historical models]()(p.309) 참고

#### Initial migrations

***`Migration.initial`***

앱의 'initial migrations'은 앱 태이블에서 처음생성된 버전의 migrations 파일: 보통은 하나의 initial migration을 갖지만 몇몇 복잡한 모델에서는 두개나 여러개를 가질수도 있다.

initial migrations은 `initial = True` 클래스 속성을 가짐. 이 속성을 못찾으면 그냥 앱에서 가장 먼저 migration 된 것을 initial로 인식함. 

만약 `migrate --fake-initial` 옵션을 사용하면 이 migrations은 특별 취급: for an initial migration that adds one or more ﬁelds (AddField operation), Django checks that all of the respective columns already exist in the database and fake- applies the migration if so. Without --fake-initial, initial migrations are treated no differently from any other migration.

`--fake`: 꼬여있는 dependency를 풀어주고 그 레벨로 다시 시작. 



#### migrate 명령어들

--database 

DATABASE Speciﬁes the database to migrate. Defaults to default.

**--fake **

Tells Django to mark the migrations as having been applied or unapplied, but without actually running the SQL to change your database schema.

This is intended for advanced users to manipulate the current migration state directly if they’re manually applying changes; be warned that using --fake runs the risk of putting the migration state table into a state where manual recovery will be needed to make migrations run correctly.

--fake-initial 

Allows Django to skip an app’s initial migration if all database tables with the names of all models created by all CreateModel operations in that migration already exist. This option is intended for use when ﬁrst running mi- grations against a database that preexisted the use of migrations. This option does not, however, check for matching database schema beyond matching table names and so is only safe to use if you are conﬁdent that your existing schema matches what is recorded in your initial migration.

--run-syncdb 

Allows creating tables for apps without migrations. While this isn’t recommended, the migrations framework is sometimes too slow on large projects with hundreds of models.

--noinput, --no-input 

Suppresses all user prompts. An example prompt is asking about removing stale content types.

The --no-input alias was added.



#### History consistency

앞에 언급했던 것처럼 두 개발 브랜치가 합쳐질 때 migrations을 linearize할 필요가 있다.

Migration 의존성을 수정하면서, 무심코 엇갈린 (모순된?) history state를 만들수 있다 (migration이 어떤것에는 적용되고 몇몇 의존적인 부분에는 적용이 안된)

이런 의존성이 부정확한 상황에 장고는 이게 고쳐질 때까지 migrations을 거부하거나 새로운 migrations를 만듬.

> django 1.10.1부터 Migration consistency checks가 추가됨







### Adding migrations to apps

새 앱에 migration을 추가하는것은 straightforward: 그냥 makemigrations만 하면 된다. 

만약 이미 model과 db table이 있지만 migrations을 아직 하지 않았다면 migration을 사용하도록 convert 해줘야한다. 다음과 같이

`$python manage.py makemigrations your_app_label`

이는 앱에 새로운 initial migration을 만들어준다. 이후 `python manage.py migrate —fake-initial`을 입력하면 장고는 initial migration을 인지하고 테이블이 이미 있다는 사실을 인지한다. (`—fake-initial`을 입력하지 않으면 이미 db table이 존재하기 때문에 오류)



### Historical models (p.309)

migrations을 실행시키면, 장고는 migrations 파일에 저장된 models의 히스토리컬 버전에서 동작한다. 





### Considerations when removing model ﬁelds

'reference to historical function'과 비슷하게 custom model fields를 지우는건 오래된 migrations에 레퍼런스로 포함되어 있으면 문제가 될 수 있다.

이런 상황을 해결하기 위해서 장고는 [system checks framework]()(p.531, validagting django project)을 사용한 몇몇 모델 필드 속성을 제공한다.

모델 필드에 다음과 같이 `system_check_deprecated_details`를 추가 (????)

```python
class IPAddressField(Field):
	system_check_deprecated_details = { 
        'msg': ( 
            'IPAddressField has been deprecated. Support for it (except '
            'in historical migrations) will be removed in Django 1.9.'
		), 'hint': 'Use GenericIPAddressField instead.', # optional '
        id': 'fields.W900', # pick a unique ID for your field.

	}
```





### Data Migrations

db schema 변경할때처럼 db 자체의 데이터 수정도 가능함: "Data migrations"라고 부름.

자동으로 만들어주지 않고 RunPython으로 만들어야함.

우선 empty migration file을 만들고

`python manage.py makemigrations --empty yourappname`

파일을 열고 RunPython으로 다음과 같이 적어줌.

```python
# - * - coding: utf-8 - * - 
from __future__ import unicode_literals

from django.db import migrations, models 

def combine_names(apps, schema_editor):
	# We can't import the Person model directly as it may be a newer 
    # version than this migration expects. We use the historical version. 
    Person = apps.get_model("yourappname", "Person") 
    for person in Person.objects.all():
        person.name = "%s %s" % (person.first_name, person.last_name)
        person.save()

class Migration(migrations.Migration):
    dependencies = [ ('yourappname', '0001_initial'), ]
    operations = [ migrations.RunPython(combine_names), ]
```

완성된 후 `python manage.py migrate`를 하면 데이터가 저장됨. (Model 생성과 동시에 저장!)



#### Accessing models from other apps

다른 앱의 모델을 RunPython에서 이용하려면 마이그레이션의 dependencies를 적어줘야함. 안그러면 LookupError

```python
class Migration(migrations.Migration):
    dependencies = [  
        ('app1', '0001_initial'), 
        # added dependency to enable using models from app2 in move_m1 
        ('app2', '0004_foobar'), 
    ]

    operations = [ migrations.RunPython(move_m1), ]
```



#### More advanced migrations

 더 고수준의 migration operation이나 직접 마이그레이션 작성은 다음 참조: [migration operations referane]()(p.1080), [writing database migrations]()(p.608~)



### Squashing migrations

"Squashing is the act of reducing an existing set of many migrations down to one (or sometimes a few) migrations which still represent the same changes."

여러 마이그레이션을 하나로 모으는것 (커밋스쿼싱처럼…) 한번에 수백개의 migrations으로 move back 하기 위해서 필요?

[squashmigrations]()(p.993) 명령어 사용

*django-admin squashmigrations app_label [start_migration_name] migration_name*

```python
$ ./manage.py squashmigrations myapp 0004 
Will squash the following migrations:
- 0001_initial
- 0002_some_change
- 0003_another_change
- 0004_undo_something Do you wish to proceed? [yN] y 
Optimizing...
Optimized from 12 operations to 7 operations.
Created new squashed migration /home/andrew/Programs/DjangoTest/test/migrations/0001_ ˓→squashed_0004_undo_somthing.py You should commit this migration but leave the old ones in place; the new migration will be used for new installs. Once you are sure all instances of the codebase have applied the migrations you squashed, you can delete them.
```

스쿼싱 한 뒤에는 migrate를 하여 변화를 db에 저장해줘야함.

이런 과도기적인 스쿼시 마이그레이션을 normal migration으로 바꿔줘야하는데,

- 대체한 모든 migrations files 지우기
- 지워진 migrations files 대신에 스쿼시된 migration으로 의존성있는 migrations들 업데이트
- squashed migration에서 replaces 어트리뷰트 지우기 (이게 있으면 squashed migration임을 장고가 알수있음.)

이렇게 바꿔주기 전에 스쿼시된걸 또 스쿼시하면 안됨.





### Serializing values

migrations은 단순한 파이썬 파일 (모델의 old definition을 담은)이기 때문에 => 이를 쓰기 위해 장고는 현재의 상태를 시리얼라이즈 해서 file에 담아야함

> serialize란?
>
> 객체에 저장된 데이터를 스트림에 쓰기 위해 연속적인 데이터로 변환하는 것을 말한다. 반대로 스트림에서 데이터를 읽어 객체로 변환하는 것을 역직렬화(deserialization)라 한다.

장고가 대부분을 serialize 할 수 있지만, repr()등 몇몇 하지못하는 것들도 있다.

serialize 가능/불가능 목록 - p.313

#### Adding a deconstruct() method

*deconstruct()* 메소드를 통해서 자신만의 커스텀 인스턴스를 시리얼라이즈 할수있다.

```python
from django.utils.deconstruct import deconstructible 


@deconstructible 
class MyCustomClass(object):
    def __init__(self, foo=1):
        self.foo = foo ...

	def __eq__(self, other):
        return self.foo == other.foo
```

