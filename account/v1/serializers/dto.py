from app.models import User
from rest_framework import serializers


class UserDto(serializers.Serializer):
    class Meta:
        model = User
        fields = ('name', 'image_url', 'created_on', 'email')