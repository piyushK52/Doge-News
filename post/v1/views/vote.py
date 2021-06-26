from django.db.models.aggregates import Sum
from middleware.auth import auth_required
from post.v1.serializers.dao import CommentVoteDao, GetVoteDao, UpdateVoteDao
from django.http import response
from post.v1.serializers.dto import CommentDto, VoteDto
from middleware.response import bad_request, success
from app.models import Comment, CommentVote, Post, Vote
from rest_framework.views import APIView


class VoteCrudView(APIView):
    @auth_required()
    def put(self, request):
        attributes = UpdateVoteDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.error)

        post = Post.objects.filter(uuid=attributes.data['uuid']).first()

        if not post:
             return success({}, 'invalid post', False)

        vote = Vote.objects.filter(post_id=post.id).first()
        if not vote:
            vote = Vote.objects.create(post_id=post.id, user_id=request.user_id, value=0)
        setattr(vote, 'value', attributes.data['increment'])
        vote.save()

        vote_count = Vote.objects.filter(post_id=post.id).aggregate(Sum('value'))['value__sum']
        response = {
            'data': {
                'vote_uuid': vote.uuid,
                'post_uuid': post.uuid,
                'vote_count': vote_count
            }
        }
        return success(response, 'vote updated successfully', True)

    @auth_required()
    def get(self, request):
        attributes = GetVoteDao(data=request.query_params)

        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        post = Post.objects.filter(uuid=attributes.data['post_uuid']).first()
        if not post:
            return success({}, 'invalid post', False)
        
        vote_count = Vote.objects.filter(post_id=post.id).aggregate(Sum('value'))['value__sum']

        response = {
            'data': {
                'post_uuid': post.uuid,
                'vote_count': vote_count
            }
        }

        return success(response, 'vote fetched successfully', True)


class CommentVoteView(APIView):

    @auth_required()
    def put(self, request):
        attributes = CommentVoteDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        comment = Comment.objects.filter(uuid=attributes.data['uuid']).first()
        if not comment:
            return success({}, 'invalid comment uuid', False)

        comment_vote = CommentVote.objects.filter(comment_id=comment.id, user_id=request.user_id).first()
        if not comment_vote:
            comment_vote = CommentVote.objects.create(comment_id=comment.id, user_id=request.user_id, value=0)

        setattr(comment_vote, 'value', attributes.data['increment'])
        comment_vote.save()

        response = {
            'data': {
                'comment': CommentDto(comment).data
            }
        }

        return success(response, 'vote updated successfully', True)