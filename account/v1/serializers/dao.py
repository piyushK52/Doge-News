from typing_extensions import Required
from rest_framework import serializers


class AddUserDao(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    bio = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=45)


class UpdateUserDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=255)
    bio = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)


class UUIDDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)


class AddPostDao(serializers.Serializer):
    caption = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    video_url = serializers.CharField(max_length=255)
    topic = serializers.CharField(max_length=45)
    user = serializers.CharField(max_length=45)


class UpdatePostDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    caption = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    video_url = serializers.CharField(max_length=255)


class UpdateVoteDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    increment = serializers.IntegerField()


class GetVoteDao(serializers.Serializer):
    post_uuid = serializers.CharField(max_length=100)
    user_uuid = serializers.CharField(max_length=100)