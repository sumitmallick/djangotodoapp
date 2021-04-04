from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import AbstractUser, User


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ('title','completed','scheduled_time','uid','pk')



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email','password')
