from app.models import Relationship, User
from rest_framework import serializers


class UserDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'image_url', 'created_on', 'email')


class RelationshipDto(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ('follower_user_uuid', 'followed_user_uuid')