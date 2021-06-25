from django.db import models
from rest_framework import serializers

class UserSignUpDao(serializers.Serializer):
    name = serializers.CharField(max_length=255, default="")
    email = serializers.CharField(max_length=255, default="")
    password = serializers.CharField(max_length=225, default="")
    bio = serializers.CharField(max_length=225, default="")
    image_url = serializers.CharField(max_length=225, default="")


class UserLoginDao(serializers.Serializer):
    email = serializers.CharField(max_length=255, default="")
    password = serializers.CharField(max_length=225, default="")
