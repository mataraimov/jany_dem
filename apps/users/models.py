from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=255,null=True,blank=True)
    age=models.CharField(max_length=255,null=True,blank=True)
    diagnose=models.CharField(max_length=255,null=True,blank=True)
    treatment=models.CharField(max_length=255,null=True,blank=True)
    target=models.IntegerField(null=True,blank=True)
    photo=models.CharField(max_length=255,null=True,blank=True)
    description=models.TextField(default='no description')
    balance=models.IntegerField(null=True,blank=True)

    def __repr__(self):
        return self.user

    def update_balance(self, amount):
        self.balance += amount
        self.save()