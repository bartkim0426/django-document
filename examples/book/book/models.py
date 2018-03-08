from django.db import models

# ex1) add extra manager methods
class BookManager(models.Manager):
    def title_count(self, keyword):
        return self.filter(title__icontains=keyword).count()


class Book(models.Model):
    objects = BookManager()
    title = models.CharField(max_length=100)
    num_pages = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


# ex2) modifying initial queryset
class MaleManager(models.Manager):
    def get_queryset(self):
        return super(MaleManager, self).get_queryset().filter(sex='M')


class FemailManager(models.Manager):
    def get_queryset(self):
        return super(FemailManager, self).get_queryset().filter(sex='F')


class Person(models.Model):

    name = models.CharField(max_length=100)
    sex = models.CharField(
        max_length=1,
        choices=(
            ('M', 'Male'),
            ('F', 'Femail')
        )
    )
    people = models.Manager()
    men = MaleManager()
    women = FemailManager()

    def __str__(self):
        return self.name


