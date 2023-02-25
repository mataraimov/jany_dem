from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    questionnaire=models.CharField(max_length=255,null=True,blank=True)
    evidence=models.CharField(max_length=255,null=True,blank=True)
    copy=models.CharField(max_length=255,null=True,blank=True)
    excerpt=models.CharField(max_length=255,null=True,blank=True)
    reference=models.CharField(max_length=255,null=True,blank=True)
    program=models.CharField(max_length=255,null=True,blank=True)
    photo=models.CharField(max_length=255,null=True,blank=True)
    position=models.CharField(max_length=255,null=True,blank=True)
    position_copy=models.CharField(max_length=255,null=True,blank=True)
    call=models.CharField(max_length=255,null=True,blank=True)
    appeals=models.CharField(max_length=255,null=True,blank=True)
    checks=models.CharField(max_length=255,null=True,blank=True)
    balance=models.IntegerField(null=True,blank=True)

    def __repr__(self):
        return self.title