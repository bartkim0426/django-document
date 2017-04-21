## Tablespaces (p.164)

[테이블스페이스 위키백과](https://ko.wikipedia.org/wiki/%ED%85%8C%EC%9D%B4%EB%B8%94%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4)

"**테이블스페이스**(Tablespace)는 데이터베이스 오브젝트 내 실제 데이터를 저장하는 공간이다. 이것은 [데이터베이스](https://ko.wikipedia.org/wiki/%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4)의 물리적인 부분이며, 세그먼트로 관리되는 모든 DBMS에 대해 저장소(세그먼트)를 할당한다.

데이터베이스 세그먼트는 데이터베이스 오브젝트 중의 하나이며, 테이블이나 인덱스와 같이 물리적 공간을 점유한다. 테이블스페이스는 한번 생성되면, 데이터베이스 세그먼트 생성시 이름으로 참조된다."

#### Delaring tablespaces for tables

model의 class Meta 안의 `db_tablespace`(p.1121) 옵션을 통해 만들어진다. 이 옵션은 자동으로 ManyToManyField를 만들어 테이블에 영향을 미친다.

`DEFAULT_TABLESPACE` 세팅을 통해 db_tablespace의 default value를 설정할 수 있다. 이는 빌트인 앱이나 코드를 컨트롤하기 힘든 앱들에 유용하다.

#### Declaring tablespaces for indexs

Field constructor에 db_tablespace 옵션을 통해서 필드의 column index에 다른 tablespace를 지정할 수 있다. index가 만들어지지 않으면 이 옵션은 무시된다.

위와 같이 `DEFAULT_INDEX_TABLESPACE` 세팅을 통해 db_tablespace의 기본 value를 설정 가능. 둘 다 설정되지 않으면 table의 기본 테이블스페이스로 생성된다.

#### An example

```python
class TablespaceExample(models.Model):
    name = models.CharField(max_length=30, db_index=True, db_tablespace="indexes")
    data = models.CharField(max_length=255, db_index=True)
    edges = models.ManyToManyField(to="self", db_tablespace="indexes")

	class Meta:
        db_tablespace = "tables"
```

##### Database support

PostgreSQL, Oracle은 tablespace를 지원하고, SQLite, MySQL은 지원하지 않는다. 지원하지 않는 db를 사용하면 모든 옵션을 무시