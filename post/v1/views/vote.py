from middleware.auth import auth_required
from post.v1.serializers.dao import GetVoteDao, UpdateVoteDao
from django.http import response
from post.v1.serializers.dto import VoteDto
from middleware.response import bad_request, success
from app.models import Post, Vote
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
        value = vote.value
        
        if attributes.data['increment']:
            value += attributes.data['increment']
            setattr(vote, 'value', value)
            vote.save()

        response = {
            'data': VoteDto(vote).data
        }
        return success(response, 'vote updated successfully', True)


    def get(self, request):
        attributes = GetVoteDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.error)

        vote = Vote.objects.filter(post=attributes.data['post_uuid'], user=attributes.data['user_uuid']).first()

        if not vote:
            return success({}, 'invalid post', False)

        response = {
            'data': VoteDto(vote).data
        }

        return success(response, 'vote fetched successfully', True)