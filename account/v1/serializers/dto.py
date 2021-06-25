from app.models import Relationship, UserProfile
from rest_framework import serializers


class UserDto(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name', 'image_url', 'created_on', 'email', 'bio')


class RelationshipDto(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ('follower_user_uuid', 'followed_user_uuid')