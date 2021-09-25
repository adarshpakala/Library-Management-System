from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    book_name=models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=30,null=True)
    quantity =models.IntegerField(null=True)
    author = models.CharField(max_length=100,null=True)
    isbn = models.IntegerField(null=True)

    def __str__(self):
        return self.book_name

class Studentinfo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    rollNo=models.CharField(max_length=100,null=True)
    branch=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.user.username

class Student(models.Model):
    studentinfo = models.ForeignKey(Studentinfo,on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE, null=True)
    issue_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    def __str__(self):
        return self.studentinfo.user.username





