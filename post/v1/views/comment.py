from post.v1.serializers.dao import CommentListDao
from django.db.models.aggregates import Sum
from post.v1.serializers.dto import CommentDto
from django.db import connection
from account.v1.serializers.dao import UUIDDao
from app.models import Comment, CommentVote, Vote
from middleware.response import bad_request, success
from rest_framework.views import APIView
from django.core.paginator import Paginator


class CommentCrudView(APIView):

    def post(self, request):
        attributes = AddCommentDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        comment = Comment.objects.create(**attributes.data)

        response = {
            'data': CommentDto(comment).data
        }

        return success(response, 'comment created successfully', True)


    def put(self, request):
        # feature to be added later
        2

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
    def get(self, request):
        attributes = UUIDDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        parent_comment = Comment.objects.filter(uuid=attributes.data['uuid']).first()
        vote_count = CommentVote.objects.filter(comment_uuid=attributes.data['uuid']).aggregate(Sum('value'))['value__sum']
        context = {'vote_count': vote_count}
        if not parent_comment:
            return success({}, 'invalid uuid', False)

        # write logic for fetching comments
        child_comment_list = Comment.objects.filter(parent=parent_comment.uuid).order_by("value").all()
        replies = []
        for comment in child_comment_list:
            vote = CommentVote.objects.filter(comment_uuid=attributes.data['uuid']).aggregate(Sum('value'))['value__sum']
            replies.append(
                {
                    'comment': CommentDto(comment).data,
                    'vote_count': vote 
                }
            )

        response = {
            'data': {
                'comment': CommentDto(parent_comment, context=context).data,
                'replies': replies
            } 
        }

        return success(response, 'comment fetched successfully', True)



class CommentListView(APIView):

    def get(self, request):
        # fetching all the comments (not their replies) for a post
        attributes = CommentListDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        comment_list = Comment.objects.filter(post_uuid=attributes.data['post_uuid']).all()

        data_per_page = 20
        paginator = Paginator(comment_list, data_per_page)
        if attributes.data['page'] > paginator.num_pages:
            return success({}, "invalid page number", False)
        
        paged_comment_object_list = paginator.page(attributes.data['page']).object_list
        paged_comment_list = []
        for comment in paged_comment_object_list:
            vote = CommentVote.objects.filter(comment_uuid=attributes.data['uuid']).aggregate(Sum('value'))['value__sum']
            paged_comment_list.append(
                {
                    'comment': CommentDto(comment).data,
                    'vote_count': vote
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