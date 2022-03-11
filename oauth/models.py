from operator import mod
from statistics import mode
from tkinter.tix import Tree
from django.db import models
from django.utils import timezone

# Create your models here.
class UserAccount(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=15)
    grant_type = models.CharField(max_length=10, default="password")
    client_id = models.CharField(max_length=5)
    client_secret = models.CharField(max_length=5)

class Session(models.Model):
    id = models.IntegerField(primary_key=True)
    akun = models.OneToOneField(UserAccount, on_delete=models.CASCADE, default="")
    access_token = models.CharField(max_length=40)
    refresh_token = models.CharField(max_length=40)
    expires_in_seconds = models.IntegerField(default=300)
    login_time = models.DateTimeField(default=timezone.now)
    
class Profile(models.Model):
    akun = models.OneToOneField(UserAccount, on_delete=models.CASCADE, default="")
    full_name = models.CharField(max_length=30)
    npm = models.CharField(max_length=10)