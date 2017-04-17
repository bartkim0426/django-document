## Field lookups

| lookup      | example                                  |                             |
| ----------- | ---------------------------------------- | --------------------------- |
| exact       | Entry.objects.get(id__exact=10)          |                             |
| iexact      | Blog.objects.get(name__iexact='beatles'), | Case-insensitive (대소문 구별없음) |
| contains    | Entry.objects.get(headline__contains='Lennon') |                             |
| icontains   | Entry.objects.get(headline__icontains='lennon') |                             |
| in          | Entry.objects.filter(in__in=[1, 2, 3])   |                             |
| gt          | Entry.objects.filter(id__gt=4)           | grater than                 |
| gte         |                                          | greater than or equal       |
| lt          |                                          | less than                   |
| lte         |                                          | less than or equal          |
| startswith  | Entry.objects.filter(headline__startswith='Will') |                             |
| istartswith |                                          | Case-insensitive            |
| endswith    | Entry.objects.filter(headline__endswith='cats |                             |
| iendswith   |                                          |                             |
| range       | Entry.objects.filter(pub_date__range=(start_date, end_date)) |                             |
| date        | Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1)) |                             |
| year        | Entry.objects.filter(pub_date\__year__gte=2005) | gte 등과 함께 사용 가능             |
| month       |                                          |                             |
| day         |                                          |                             |
| week_day    |                                          |                             |
| hour        |                                          |                             |
| minute      |                                          |                             |
| second      |                                          |                             |
| isnull      | Entry.objects.filter(pub_date__isnull=True) |                             |
| search      | Entry.objects.filter(headline__search="+Django -jazz Python") |                             |
| regex       | Entry.objects.get(title__regex=r'^(An?\|The) +') |                             |
| iregex      |                                          |                             |
|             |                                          |                             |

