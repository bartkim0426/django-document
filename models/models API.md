### Models API (p1128)

너무 어려운 내용들이 많아서… 점차 더 공부하자!

#### create objects
Add a method on a custom manager (usually preferred):

```python
class BookManager(models.Manager):
	def create_book(self, title):

	book = self.create(title=title) # do something with the book return book
	
	
class Book(models.Model):
	title = models.CharField(max_length=100)
	
	objects = BookManager() # 만든 bookmanager를 불러줘야 적용이 된다.
	
	book = Book.objects.create_bowok("Pride and Prejudice")
```

####Customizing model loading

`classmethod Model.from_db(db, ﬁeld_names, values)`

무슨 말인지 잘 모르겠다… ㅠㅠ 물어보자

#### 모델 지우기

If you delete a ﬁeld from a model instance, accessing it again reloads the value from the database:

```python
obj = MyModel.objects.first()

del obj.field

obj.field # Loads the field from the database
```