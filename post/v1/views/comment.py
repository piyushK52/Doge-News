from middleware.auth import auth_required
from post.v1.serializers.dao import AddCommentDao, CommentListDao
from django.db.models.aggregates import Sum
from post.v1.serializers.dto import CommentDto
from django.db import connection
from account.v1.serializers.dao import UUIDDao
from app.models import Comment, CommentVote, Post, Vote
from middleware.response import bad_request, success
from rest_framework.views import APIView
from django.core.paginator import Paginator


class CommentCrudView(APIView):

    @auth_required()
    def post(self, request):
        attributes = AddCommentDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        post = Post.objects.filter(uuid=attributes.data['post_uuid']).first()
        if not post:
            return success({}, 'invalid post uuid', False)
        
        parent_comment_id = None
        if attributes.data['parent_comment_uuid']:
            parent_comment = Comment.objects.filter(uuid=attributes.data['parent_comment_uuid']).first()
            if parent_comment:
                parent_comment_id = parent_comment.id

        comment = Comment.objects.create(post_id=post.id, user_id=request.user_id, parent_comment_id=parent_comment_id, content=attributes.data['content'])

        response = {
            'data': CommentDto(comment).data
        }

        return success(response, 'comment created successfully', True)

    @auth_required()
    def put(self, request):
        # feature to be added later
        2

    @auth_required()
    def delete(self, request):
        attributes = UUIDDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        comment = Comment.objects.filter(uuid=attributes.data['uuid']).first()
        if not comment:
            return success({}, 'invalid uuid', False)

        comment.delete()

        return success({}, 'comment deleted successfully', True)

    # fetches a particular comment and its children
    @auth_required()
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        parent_comment = Comment.objects.filter(uuid=attributes.data['uuid']).first()
        if not parent_comment:
            return success({}, 'invalid uuid', False)

        child_comment_list = Comment.objects.filter(parent_comment_id=parent_comment.id).all()
        replies = []
        for comment in child_comment_list:
            replies.append(
                {
                    'comment': CommentDto(comment).data,
                }
            )

        response = {
            'data': {
                'comment': CommentDto(parent_comment).data,
                'replies': replies
            } 
        }

        return success(response, 'comment fetched successfully', True)



class CommentListView(APIView):

    @auth_required()
    def get(self, request):
        # fetching all the comments (not their replies) for a post
        attributes = CommentListDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        post = Post.objects.filter(uuid=attributes.data['post_uuid']).first()
        if not post:
            return success({}, 'invalid post uuid', False)

        comment_list = Comment.objects.filter(post_id=post.id, parent_comment_id=None).all()

        data_per_page = 20
        paginator = Paginator(comment_list, data_per_page)
        if attributes.data['page'] > paginator.num_pages:
            return success({}, "invalid page number", False)
        
        paged_comment_object_list = paginator.page(attributes.data['page']).object_list
        paged_comment_list = []
        for comment in paged_comment_object_list:
            paged_comment_list.append(
                {
                    'comment': CommentDto(comment).data,
                }
            )


        response = {
            'data_per_page': data_per_page,
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': attributes.data['page'],
            'data': paged_comment_list
        }

        return success(response, "comment list fetched successfully", True)