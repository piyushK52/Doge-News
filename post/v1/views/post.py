from django.db.models.aggregates import Sum
from post.service import remove_all_post_activity
from account.v1.serializers.dto import PostDto
from app.models import Post, Vote
from account.v1.serializers.dao import AddPostDao, UUIDDao, UpdatePostDao
from middleware.response import bad_request, error, success
from rest_framework.views import APIView


class PostCrudView(APIView):

    def post(self, request):
        attributes = AddPostDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.error)

        post = Post.objects.create(**attributes.data)
        
        response = {
            'data': PostDto(post).data
        }

        return success(response, "post created successfully", True)

    
    def put(self, request):
        attributes = UpdatePostDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        post = Post.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()

        if not post:
            return success({}, 'invalid post', False)

        for attr, value in attributes.data.items():
            setattr(post, attr, value)
        post.save()

        response = {
            'data': PostDto(post).data
        }
        return success(response, 'post updated successfully', True)


    def delete(self, request):
        attributes = UUIDDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        post = Post.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not post:
            return success({}, 'invalid uuid', False)

        post.is_disabled = True
        post.save()

        remove_all_post_activity(post.id)

        return success({}, 'account deleted successfully', True)


    def get(self, request):
        attributes = UUIDDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        post = Post.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not post:
            return success({}, 'invalid uuid', False)

        # fetching upvotes/downvotes of this post
        vote_count = Vote.objects.filter(post_uuid=attributes.data['uuid']).aggregate(Sum('value'))['value__sum']

        user_vote = Vote.objects.filter(post_uuid=attributes.data['uuid'], user_uuid=request.user.uuid).first().value

        data = {
            'post': PostDto(post).data,
            'vote': {
                'vote_count': vote_count,
                'user_vote': user_vote
            }
        }
        
        response = {
            'data': data
        }

        return success(response, 'post fethced successfully', True)