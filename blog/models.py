from django.db import models
from django.db.models.fields import DateField

class Forms(models.Model):
    email=models.EmailField(max_length=100,default='hello@hello.com')
    name=models.CharField(max_length=100,default='name')
    desc=models.CharField(max_length=100,default='desc')
    date=models.DateField()

    def __str__(self):
        return self.name
class Book(models.Model):
    bookname=models.CharField(max_length=125)
    bookauthor=models.CharField(max_length=125)
    serial=models.IntegerField()

    def __str__(self):
        return self.bookname