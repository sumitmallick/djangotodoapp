from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    completed = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(null=True,blank=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.title+" | "+str(self.completed)
