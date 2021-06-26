from django.db.models.aggregates import Count, Sum
from rest_framework import serializers
from app.models import Comment, CommentVote, Post, Vote, Topic


class VoteDto(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('uuid',)


class TopicDto(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('uuid', 'title', 'desc', 'url', 'category', 'created_on', 'source_name')


class PostDto(serializers.ModelSerializer):
    topic = TopicDto()
    vote_count = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('uuid', 'caption', 'image_url', 'video_url', 'created_on', 'topic', 'vote_count', 'user_vote')

    def get_vote_count(self, obj):
        vote_count = Vote.objects.filter(post_id=obj.id).aggregate(Sum('value'))['value__sum']
        if not vote_count:
            vote_count = 0
        return vote_count
    
    def get_user_vote(self, obj):
        user_vote = Vote.objects.filter(post_id=obj.id, user_id=obj.user_id).first().value
        if not user_vote:
            user_vote = 0
        return user_vote


class CommentDto(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('uuid', 'vote_count', 'content', 'reply_count')

    def get_reply_count(self, obj):
        if obj.parent_comment_id != None:
            return None
        reply_count = Comment.objects.filter(parent_comment_id=obj.id).all().count()
        return reply_count
    
    def get_vote_count(self, obj):
        vote_count = CommentVote.objects.filter(comment_id=obj.id).aggregate(Sum('value'))['value__sum']
        if not vote_count:
            vote_count = 0
        return vote_count