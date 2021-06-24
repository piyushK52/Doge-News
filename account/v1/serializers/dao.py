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