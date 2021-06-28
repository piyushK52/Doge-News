from app.models import Relationship, UserProfile
from rest_framework import serializers


class UserDto(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name', 'image_url', 'created_on', 'email', 'bio')


class RelationshipDto(serializers.ModelSerializer):
    follower_uuid = serializers.SerializerMethodField()
    followed_uuid = serializers.SerializerMethodField()

    class Meta:
        model = Relationship
        fields = ('follower_uuid', 'followed_uuid')

    def get_follower_uuid(self, obj):
        user = UserProfile.objects.filter(id=obj.follower_user_id).first()
        if not user:
            return None
        return user.uuid
    
    def get_followed_uuid(self, obj):
        user = UserProfile.objects.filter(id=obj.followed_user_id).first()
        if not user:
            return None
        return user.uuid
