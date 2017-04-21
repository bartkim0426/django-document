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
- *[they are evaluated]()*: p.1139