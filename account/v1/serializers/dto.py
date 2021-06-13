from app.models import Like, Post, Topic, User, Vote
from rest_framework import serializers


class UserDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'image_url', 'created_on', 'email')


class TopicDto(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'desc', 'url', 'category', 'source_name')


class PostDto(serializers.ModelSerializer):
    topic = TopicDto()
    
    class Meta:
        model = Post
        fields = ('caption', 'image_url', 'video_url', 'created_on')


class VoteDto(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('post_uuid', 'value')


class TopicDto(serializers.ModelSerializer):
    class Meta:
        meta = Topic
        fields = ('title', 'desc', 'url', 'category', 'created_on', 'source_name')
