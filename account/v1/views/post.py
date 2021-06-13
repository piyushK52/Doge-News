from account.service import remove_all_post_activity
from account.v1.serializers.dto import PostDto
from app.models import Post
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
        attributes = UUIDDao(data=request.query_params)
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
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        post = Post.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not post:
            return success({}, 'invalid uuid', False)
        
        response = {
            'data': PostDto(post).data
        }

        return success(response, 'post fethced successfully', True)