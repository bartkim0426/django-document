## Database transactions

 [트랜젝션이란?](http://www.incodom.kr/%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98): 뜻을 몰라서 괜찮게 설명되있는 블로그를 참고했습니다.

( p.145~)

장고는 데이터 베이스 트랜잭션을 위해 몇가지 방법을 제공한다

#### Managing database transctions

#### django's default transaction behavior

장고의 default behavior: autocommit mode => 각각의 query는 즉각적으로 db에 코밋된다.

#### Trying transactions to HTTP requests

`ATOMIC_REQUESTS = True`로 해놓으면 각각의 request를 트랜잭션 처리한다. 

동작 방법은 다음과 같다: view function을 부르기 전에, 장고는 transaction을 시작한다. response가 문제 없이 생성되면 트랜젝션을 코밋하고, view에서 문제가 생기면 장고는 트랜젝션을 롤백한다.

실제 사용될 때 모든 view에 atomic() 데코레이터가 적용되기 때문에 특정 view에서 이를 방지시킬 수 있다. (`non_atomic_requests`를 사용)

```python
from django.db import transaction

@transaction.non_atomic_requests
def my_view(request):
    do_stuff()
```

#### Controling transactions explicitly

장고는 database 트랜젝션을 컨트롤하기 위한 single API들을 제공한다.

**atomic**(*using=None, savepoint=True*)

"Atomicity is the defining property of db transaction."(??) 

atomic은 db의 atomictiy(원자성)이 보장하는 코드 블럭을 만들어준다. 만약 코드 블럭이 성공적으로 완성되면, 변화가 db에 코밋된다. 오류가 있으면 롤백되고...

atomic 블럭은 nested 가능하다(?): 블록 안이 성공적으로 완료되도 코드 블록 밖에서 exception이 발생하면 롤백이 발생한다. 

atomic은 decorator, context manager 둘 다 사용 가능하다 (예시처럼)

```python
from django.db import transaction

@transaction.atomic
def viewfunc(request):
    # 여기에 있는 코드는 트랜젝션으로 실행
    dO_stuff()
    
def viewfunc2(request):
    # 여기에 있는 코드는 장고의 default인 autocommit mode
    do_stuff()
    
    with transaction.atomic():
        # 여기의 코드는 트랜젝션으로 구동
        do_more_stuff()
```

atomic을 try/except 문으로 감싸면 에러 핸들링하기에 좋다.

```python
from django.db import IntegrityError, transaction 

@transaction.atomic 
def viewfunc(request):
    create_parent()
    
    try:
        with transaction.atomic():
            generate_relationships() 
        except IntegrityError:
            handle_exception()
    
    add_children()
```

> Atomic 안에서 exception catching을 피해야한다.
>
> 만약 atomic 내부에서 에러가 발생하면 장고가 어디에서 에러가 발생했는지 정확하게 발견을 못할수 있기 때문에

atomicity를 보장하기 위해서 atomic은 몇몇 API들을 disable시킨다: commit, roll back, change atucommic 시도 등을 atomic 내부에서 하면 예외가 발생한다.

atomic은 using argument로 database의 이름을 받는다. 만약 없으면 장고는 default db를 사용한다. 



### Autocommit (p.147)

#### Why django uses autocommit

SQL문에서, 각각의 SQL 쿼리들은 트랜젝션을 구동시키고 commit이나 roll back되야한다 => 이는 앱개발에서 편리한 방법이 아니기 때문에 이를 경감시키기 위해서 많은 db들이 autocommit mode를 제공. 

[PEP249](https://www.python.org/dev/peps/pep-0249/)(Python db API specification v2.0)은 autocommit이 기본적으로 꺼져있음 -> 장고는 이를 on으로 overide한다. 이를 deactivate 시킬 수 있지만, 비추한다.

#### Deactivating transaction management

configuration에서 AUTOCOMMIT=False로 오토커밋을 정지시킬 수 있다 => 그렇게 되면 써드파티 라이브러리를 포함한 장고의 모든 트랜젝션의 커밋이 꺼짐… 그래서 트랜젝션 컨트롤 미들웨어를 조정하는게 좋다.

#### Performing actions after commit

트랜젝션이 성공적으로 코밋 된 이후에만 db에 특정 액션을 취하고 싶다면 `on_commit(func, using=None)`  func를 사용 가능하다.

```python
from djangodb import transaction

def do_sth():
    pass

transaction.on_commit(do_sth)
# 다음처럼 lambda 식을 활용할 수 있다.
transaction.on_commit(lambda: some_celery_task.delay('arg1'))
```



#### Savepoints

"만약 INSERT 작업을 한 다음 'SAVEPOINT A'라는 명령을 실행하였다면 나중에 'ROLLBACK A'라는 명령을 통해 INSERT 작업을 한 그 위치로 되돌아 올 수 있는 것이죠. 그 전에 'COMMIT' 명령을 실행하지 않았다면 말입니다." ([it지식공유](http://www.itmembers.net/board/view.php?id=oracle&page=1&sn1=&divpage=1&sn=off&ss=on&sc=on&select_arrange=headnum&desc=asc&no=40&PHPSESSID=597d3b24c7da605e4b211d816a427898))

(p.148)

#### Order of execution

#### Exception handling (p.149)

한 트랜젝션 내의 function에서 예외가 발생하면 같은 트랜잭션 내의 다른 함수들은 더이상 실행되지 않는다. 

#### timing of execution

#### Use in tests

#### Why no rollback hook?



#### Low-level APIs (p.150)

> 가능하다면 항상 atomic()을 사용하는게 좋다. Low level API는 자신만의 트랜잭션 매니지먼트를 만들때만 쓰는게 좋다. 

#### Autocommit

`get_autocommit(using=None)`, `set_autocommit(autocommit, using=None)`을 사용해서 autocommit을 끌 수 있다. (using argument에는 db 이름이 들어가야함) 이를 끄면 django는 더이상 도움을 주지 못하고 직접 commit(), rollback() 등을 사용해야한다.

atomic() 코드 블록이 active하다면, autocommit이 꺼지지 않는다. 

#### Transactions

`django.db.transaction`의 commit(), rollback()을 활용해서 트랜젝션 중에 변경사항을 적용시킬 수 있다. 

#### savepoints

savepoints는 롤백을 가능하게 하는 트랜잭션의 마커: SQLite, PostgreSQL, Oracle, MySQL에서 사용 가능하다.

autocommit에서는 별로 쓸모가 없지만 atomic()으로 트랜잭션을 열면 commit, rollback을 기다리는 여러 db operations을 만들 수 있다 (?)

atomic() 데코레이터가 사용되면 부분적으로 commit/rollback할 수 있는 savepoint를 만들어준다. 이 방법 (atomic)을 사용하는 것을 강력하게 추천하지만, 아래 나온 API들을 사용할 수 있긴 하다… (p.151)

**savepoint**(*using=None*)

**savepoint_commit**(*sid, using=None*)

**savepoint_rollback**(*sid, using=None*)

**clean_savepoints**(*using=None*)

#### Database-specific notes: p.152 참고

Savepoints in SQLite, Transactions in MySQL, Handling exceptions within PostgreSQL transactions, 

#### Transaction rollback 

```python
a.save()
try:
    b.save()
except IntegrityError:
    transaction.rollback()
c.save()
```

#### Savepoint rollback

```python
a.save()
sid = transaction.savepoint()
try:
    b.save()
    transaction.savepoint_commit(sid)
except IntegritryError:
    transaction.savepoint_rollback(sid)
c.save()
```

s