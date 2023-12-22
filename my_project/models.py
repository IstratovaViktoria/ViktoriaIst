from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    address = models.CharField(max_length=100, verbose_name="address location",
                               help_text="Введите адрес", null=False, blank=False)

    def __str__(self):
        return "Location" + self.address

    class Meta:
        db_table = "Location"


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name="name country",
                            help_text="Введите название страны", null=False, blank=False)

    def __str__(self):
        return "Country" + self.name

    class Meta:
        db_table = "Country"


class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name="name author",
                            help_text="Введите имя автора", null=False, blank=False)
    last_name = models.CharField(max_length=100, verbose_name="last_name author",
                                 help_text="Введите фамилию автора", null=False, blank=False)
    gender = models.CharField(max_length=50, verbose_name="gender",
                              help_text="Введите пол", null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="country author",
                                help_text="Выберите страну", null=False, blank=False)

    def __str__(self):
        return "Author" + self.name

    class Meta:
        db_table = "Author"


class Publishing(models.Model):
    name = models.CharField(max_length=50, verbose_name="name publishing_house",
                            help_text="Введите название издательства", null=False, blank=False)

    def __str__(self):
        return "Publishing" + self.name

    class Meta:
        db_table = "Publishing"


class Book(models.Model):
    name = models.CharField(max_length=50, primary_key=True, verbose_name="name book",
                            help_text="Введите название книги", null=False, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="author book",
                               help_text="Выберите имя автора книги", null=False, blank=False)
    page = models.PositiveIntegerField(verbose_name="page",
                                       help_text="Введите количество страниц", null=False, blank=False)
    publishing = models.ForeignKey(Publishing, on_delete=models.CASCADE, verbose_name="publishing_house book",
                                   help_text="Выберите название издательства", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='id User',
                                help_text='выберите id пользователя', null=True, blank=True)

    def __str__(self):
        return "Book" + self.name

    class Meta:
        db_table = "Book"


class Buyer(models.Model):
    name = models.CharField(max_length=50, verbose_name="name buyer",
                            help_text="Введите имя покупателя", null=False, blank=False)
    last_name = models.CharField(max_length=100, verbose_name="last_name buyer",
                                 help_text="Введите фамилию покупателя", null=False, blank=False)
    gender = models.CharField(max_length=50, verbose_name="gender",
                              help_text="Введите пол", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='id User',
                                help_text='выберите id пользователя', null=True, blank=True)

    def __str__(self):
        return "Buyer" + self.name

    class Meta:
        db_table = "Buyer"


class Literature(models.Model):
    name_literature = models.CharField(max_length=50, verbose_name="name literature",
                                       help_text="Введите название литературы", null=False, blank=False,
                                       primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name="buyer",
                              help_text="Выберите покупателя", null=False, blank=False)
    publishing = models.ManyToManyField(Publishing)

    class Meta:
        db_table = "Literature"


class Store(models.Model):
    number = models.PositiveIntegerField(verbose_name="number",
                                         null=False, blank=False)
    name = models.CharField(max_length=50, verbose_name="name store",
                            help_text="Введите название магазина", null=False, blank=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="location store",
                                 help_text="Выберите местоположение адреса", null=False, blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="book",
                             help_text="Выберите название книги", null=False, blank=False)
    cost = models.PositiveIntegerField(verbose_name="cost",
                                       help_text="Введите цену", null=False, blank=False)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE, verbose_name="literature",
                                   help_text="Выберите литературу", null=False, blank=False, default="Книги",
                                   db_column="literature")

    def __str__(self):
        return "Store" + self.name

    class Meta:
        db_table = "Store"
