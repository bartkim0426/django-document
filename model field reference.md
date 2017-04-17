### Model Field Reference (1092p)

### Field options



|                  |                        |                                          |
| ---------------- | ---------------------- | ---------------------------------------- |
| null             | Field.null             | True일 경우에 NULL이 db에 저장됨. CharField, TextField에서 사용 안하는게 좋음 (empty string은 null이 아니기 때문에). |
| blank            | Field.blank            | True일 경우에 blank를 허용. null/blank 차이점- null은 database-related, blank는 validation-related. blank=True일 경우 field에 empty value가 들어간다. (값이 존재) |
| choices          | Field.choices          | 2 item이 있는 list, tuple을 사용함. default form으로 select box가 사용됨. 튜플의 첫 번째 값은 model의 실제 value, 두번째 값은 human-readable name. 자세한 내용은 아래에 |
| db_colum         | Field.db_column        | Database column의 이름을 지정할 수 있다. 비워놓으면 장고가 기본으로 생성 |
| db_index         | Field.db_index         | True일 경우 database index가 생성됨             |
| db_tablespace    | Field.db_tablespace    |                                          |
| default          | Field.default          | value, callable object가 들어갈 수 있음. list, set과 같은 mutable object는 쓸 수 없기 때문에 함수로 만들어서 호출해야함. (JSONField같이). ForeignKey같은 필드에서는 모델 인스턴스가 아닌 value(pk)값이 들어가줘야함 |
| editable         | Field.editable         | default=True, False일 경우 필드에 보여지지 않음      |
| error_message    | Field.error_messages   |                                          |
| help_text        | Field.help_text        | Extra help text. 위젯에 보여짐.                |
| primary_key      | Field.primary_key      | True면 model에 primary key로 됨 => null=False, unique=True를 내제함. |
| unique           | Field.unique           | True일 경우 db_index를 설정할 필요 없음             |
| unique_for_date  | Field.unique_for_date  | DataField, DateTimeField가 세팅되어있어야함.  title에 설정 되어있으면 (`unique_for_date="pub_date"`) 두 레코드가 같은 title, pub_date를 가지지 못하게. |
| unique_for_month | Field.unique_for_month |                                          |
| unique_for_year  | Field.unique_for_year  |                                          |
| verbose_name     | Field.verbose_name     | 필드의 human-readable 이름. 설정을 안하면 자동으로 _ (underscore)을 스페이스로 전환해서 만들어줌. |
| validators       | Field.validators       | 필드에 적용되는 validators 리스트. 자세한건 참조 문서 (p.1377) |
|                  |                        |                                          |

- choices

아래 예시처럼 model class 안에서 choices를 명시해주는것이 좋다. (다른 곳에서 쉽게 접근 가능하다. `Student.SOPHOMORE`처럼)



### Field types

```python
from django.db import models 

class Student(models.Model):
    FRESHMAN = 'FR' 
    SOPHOMORE = 'SO' 
    JUNIOR = 'JR' 
    SENIOR = 'SR' 
    YEAR_IN_SCHOOL_CHOICES = (
      (FRESHMAN, 'Freshman'),
      (SOPHOMORE, 'Sophomore'),
      (JUNIOR, 'Junior'),
      (SENIOR, 'Senior'),
    ) 
    year_in_school = models.CharField(
    max_length=2,
    choices=YEAR_IN_SCHOOL_CHOICES,
    default=FRESHMAN, 
    )

    def is_upperclass(self):
	    return self.year_in_school in (self.JUNIOR, self.SENIOR)
```

다음과 같이 group으로 받을 수 있음

```python
MEDIA_CHOICES = (
('Audio', ( ('vinyl', 'Vinyl'), 
           ('cd', 'CD'), 
          )
), 
('Video', (
		('vhs', 'VHS Tape'), 
    	('dvd', 'DVD'), 
		), 
 ('unknown', 'Unknown'),
)
```

=> 이렇게 되면 Audio 탭에서 vinyl, cd / Vidio 탭에서 vhs, dvd를 받을 수 있다. 카테고리 선택할 때 이런 방식으로 넣어줘도 괜찮겠다… 

`blank=False`로 되어있지 않고 default 값이 설정이 안 되어있으면 자동으로 "———----"라벨을 만들어서 첫 화면에 이게 선택되어있음. override 하려면 choices tuple에 None을 추가 ex) `(None, 'Your string for display')` => CharField에서는 None 대신에 '' (empty string)을 넣어줘야한다.





| field name                 | 사용 (only required)                       | 비고                                       |
| -------------------------- | ---------------------------------------- | ---------------------------------------- |
| AutoField                  |                                          | primary key에서 사용됨                        |
| BigAutoField               |                                          | 64-bit로 사용되는 AutoField                   |
| BigIntegerField            |                                          |                                          |
| BinaryField                |                                          | raw binary data 저장하는 필드. bytes assignment만 지원함. |
| BooleanField               |                                          | default form widget: CheckboxInput. null을 받으려면 NullBooleanField를 사용 |
| **CharField**              | max_length                               | Lagre amount: TextField 사용, default widget은 TextInput |
| CommaSeparatedIntegerField | max_length                               | 콤마로 구분된 integer들의 필드. `validators=[validate_comma_seperated_integer_list]`가 적용된 CharField |
| DateField                  |                                          | datetime.date 인스턴스를 받는 필드. 옵션으로 auto_now(object가 save 될때 자동으로 셋. 보통 last-modified에 사용), auto_now_add 받음(처음 생성될 때만 셋됨.  creation timestamps에서 주로 사용.) default timezone의 date를 사용. |
| **DateTimeField**          |                                          | datetime.datetime 인스턴스를 받는 필드. 위의 DateField와 거의 동일 |
| DecimalField               | max_digits=None, decimal_places=None,    | [Decimal](https://docs.python.org/3/library/decimal.html#decimal.Decimal) 인스턴스? … ㅠㅠ 뭔지 잘 모르겠다 |
| DurationField              |                                          | [datetime.timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta) 안의 모델. periods of time을 저장하는 필드. PostgreSQL 사용시에 interval 데이터 타입 사용 |
| **EmailField**             | max_length=254                           | Valid email인지 validate 해주는 charfield. EmailValidator를 사용. (P1378) |
| **FileField**              | 예시 아래 참조                                 | 파일 업로드 필드. upload_to(업로드 디렉토리와 파일 명을 지정해주는 attribute. 함수로도 사용 가능하다.  자세한 내용은 1096p.) / storage (저장해주는 기능) 두가지 argument: 아래 자세히 설명 |
| FieldFile                  |                                          | 모델에서 FileField로 access 하면 FieldFile 인스턴스가 주어짐. 아래 더 자세히 설명 |
| FilePathField              | class FilePathField(path="home/image",)  | 특정 디렉토리의 파일명에 제한된 CharField. 여러 argument 중 path는 필수, match, recursize, allow_files, allow_folders는 option. |
| FloatField                 |                                          | python float instance를 받는 floating-point num |
| ImageField                 |                                          | FileField의 모든 메소드, 속성 상속받음 + valid image일 경우에 validate 해줌. height, width 속성도 가짐. [Pillow](https://pillow.readthedocs.io/en/latest/) 라이브러리 필요. |
| IntegerField               |                                          | Values from -2147483648 to 2147483647 are safe |
| GenericIPAddressField      | `class GenericIPAddressField(protocol=’both’, unpack_ipv4=False, **options).` | IPv4, IPv6 주소를 str 포맷으로 받아줌.             |
| NullBooleanField           |                                          | BooleanField와 비슷하지만 NULL을 허용.            |
| PositiveIntegerField       |                                          | 0이나 양수를 받아줌                              |
| PositiveSmallIntegerField  |                                          | 0~32767까지의 양수 받아줌 (왜있는거지?)               |
| SlugField                  | `class SlugField(max_length=50)`         | Max_length 지정 안하면 자동으로 50. 보통 자동으로 생성되게 함.(prepopulated_fields-아래 설명) allow_unicode 속성 있음 |
| SmallIntegerField          |                                          | -32768 ~ 32767                           |
| TextField                  |                                          | Textarea를 기본 위젯으로 받는 텍스트 필드. max_length를 지정하면 widget의 자동 생성에는 영향을 미치지만 모델, db 레벨에서는 한정 안됨. |
| TimeField                  |                                          | datetime.time 인스턴스를 받음. DateField와 유사    |
| URLField                   |                                          | URL을 위한 CharField. max_length 지정 안하면 자동으로 200 |
| UUIDField                  |                                          | ?? universally unique identifiers를 저장하기 위한 필드. PostgreSQL에서 사용시 uuid datatype으로 저장. AutoField 대용으로 쓰기 좋음? |
| **ForeignKey**             | `ForeignKey(othermodel, on_delete,)`     | 첫 argument로 다른 모델이 필수적. 자세한 설명은 아래       |
| **ManyToManyField**        | `ManyToManyField(othermodel,)`           | 첫 argument로 다른 모델. 다양한 arguments는 아래에 정리 |
| OneToOneField              | `OneToOneField(othermodel, on_delete, parent_link=False)` | 이것도 따로 정리                                |
|                            |                                          |                                          |



- FileField 예시

**FileField.upload_to**

```python
class MyModel(models.Model):
  # file will be uploaded to MEDIA_ROOT/uploads 
  upload = models.FileField(upload_to='uploads/') # or...

  # file will be saved to MEDIA_ROOT/uploads/2015/01/30 
  upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
```

함수로 upload_to를 사용 가능하다 (instance, filename을 받아서)

```python
def user_directory_path(instance, filename):
  # file will be uploaded to MEDIA_ROOT/user_<id>/<filename> 
  return 'user_{0}/{1}'.format(instance.user.id, filename)

class MyModel(models.Model):
	upload = models.FileField(upload_to=user_directory_path)
```

**FileField.sotrage**

FileField, ImageField 모델은 다음 몇 가지 단계를 거쳐야함.

1. `settings.py`에서 `MEDIA_ROOT`를 지정해줘야함. 
2. FileField, ImageField 모델의 `upload_to` 옵션에 MEDIA_ROOT의 subdirectory를 사용
3. 이제 해당 디렉토리에 저장됨. 편의를 위해서 url attribute를 사용 가능. ex) 만약 ImageField 이름이 mug_shot이라면 template에서 {{ object.mug_shot.url }} 처럼 사용

ex) `MEDIA_ROOT`가 `/home/media`로 되어있고, 

`upload_to`가 `photos/%Y/%m/%d`로 되어있으면 2017, 16, Apr에 저장된 파일은

`/home/media/photos/2017/04/16`디렉토리에 저장됨...

이 외에 name, size attribute 사용 가능; [Managing files](https://docs.djangoproject.com/en/1.11/topics/files/) 가이드 참고 (p315)

- FieldFile (p.1098)

read(), write() 이외에도 다양한 메소드 제공

 FieldFile.name,  FieldFile.size,  FieldFile.url,  FieldFile.oepn (mode = 'rb'),  FieldFile.close(),  FieldFile.save(content, save=True),  FieldFile.delete(save=True)

- prepopulated_fields ()

ModelAdmin.prepopulated_fields

```python
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
```

- ForeinKey (p.1103): 추후에 추가하기- 따로 빼서
- ManyToManyField: 추후 추가