from rest_framework import serializers
from app.models import Post, Vote, Topic


class VoteDto(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('post_uuid', 'value')


class TopicDto(serializers.ModelSerializer):
    class Meta:
        meta = Topic
        fields = ('title', 'desc', 'url', 'category', 'created_on', 'source_name')


class PostDto(serializers.ModelSerializer):
    topic = TopicDto()
    
    class Meta:
        model = Post
        fields = ('caption', 'image_url', 'video_url', 'created_on')