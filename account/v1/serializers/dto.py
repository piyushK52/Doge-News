from app.models import Like, Post, User, Vote
from rest_framework import serializers


class UserDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'image_url', 'created_on', 'email')


class TopicDto(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'desc', 'url', 'category', 'source_name')



class LikeDto(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('value')


class PostDto(serializers.ModelSerializer):
    topic = TopicDto()
    like = LikeDto()
    
    class Meta:
        model = Post
        fields = ('caption', 'image_url', 'video_url', 'created_on')


class VoteDto(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('post', 'value')
