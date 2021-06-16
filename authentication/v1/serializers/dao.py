from django.db import models
from rest_framework import serializers

class UserSignUpDao(serializers.Serializer):
    name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=45, default="")


class UserLoginDao(serializers.Serializer):
    email = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=45, default="")
