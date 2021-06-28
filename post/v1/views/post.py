from account.v1.serializers.dao import UUIDDao
from middleware.auth import auth_required
from post.v1.serializers.dao import AddPostDao, PostListDao, UpdatePostDao
from django.core.paginator import Paginator
from django.db.models.aggregates import Sum
from django.db.models.fields import NullBooleanField
from post.service import remove_all_post_activity
from post.v1.serializers.dto import PostDto
from app.models import Comment, Post, Topic, Vote
from middleware.response import bad_request, error, success
from rest_framework.views import APIView


class PostCrudView(APIView):
    @auth_required()
    def post(self, request):
        attributes = AddPostDao(data=request.data)
        print("attirbutes found--> ", attributes)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        dao_obj = attributes.data
        dao_obj['user_id'] = request.user_id

        topic = Topic.objects.filter(uuid=dao_obj['topic_uuid'], is_disabled=False).first()
        if not topic:
            return success({}, 'invalid topic uuid', False)
        dao_obj['topic_id'] = topic.id
        del dao_obj['topic_uuid']
        post = Post.objects.create(**dao_obj)
        
        response = {
            'data': PostDto(post).data
        }

        return success(response, "post created successfully", True)

    @auth_required()
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

    @auth_required()
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

    @auth_required()
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


class PostListView(APIView):
    @auth_required()
    def get(self, request):
        # fetching posts through pagination
        attributes = PostListDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        post_list = Post.objects.all()

        data_per_page = 6
        paginator = Paginator(post_list, data_per_page)
        if attributes.data['page'] > paginator.num_pages:
            return success({}, "invalid page number", False)
        
        paged_post_object_list = paginator.page(attributes.data['page']).object_list

        response = {
            'data_per_page': data_per_page,
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': attributes.data['page'],
            'data': PostDto(paged_post_object_list, many=True).data
        }

        return success(response, "post list fetched successfully", True)