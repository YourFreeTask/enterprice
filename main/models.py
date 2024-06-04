from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    token = models.CharField(max_length=100)

class Project(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    users = models.ManyToManyField(User, related_name='projects')

class Task(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Transaction(models.Model):
    project = models.ManyToManyField(Project, related_name='transactions')
    task = models.ManyToManyField(Task, related_name='transactions')
    time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)

class Done(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, related_name='history')

    class Meta:
        verbose_name_plural = 'Done'

class Entrance(models.Model):
    user = models.ManyToManyField(User, related_name='LogIn')
    time = models.DateTimeField(auto_now_add=True)
