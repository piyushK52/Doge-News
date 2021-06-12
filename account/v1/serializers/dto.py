from app.models import Like, Post, User
from rest_framework import serializers


class UserDto(serializers.Serializer):
    class Meta:
        model = User
        fields = ('name', 'image_url', 'created_on', 'email')


class TopicDto(serializers.Serializer):
    class Meta:
        model = Post
        fields = ('title', 'desc', 'url', 'category', 'source_name')



class LikeDto(serializers.Serializer):
    class Meta:
        model = Like
        fields = ('value')


class PostDto(serializers.Serializer):
    topic = TopicDto()
    like = LikeDto()
    
    class Meta:
        model = Post
        fields = ('caption', 'image_url', 'video_url', 'created_on')

