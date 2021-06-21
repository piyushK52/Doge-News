from middleware.auth import auth_required
from account.v1.serializers.dto import TopicDto
from account.v1.serializers.dao import AddTopicDao, UUIDDao, UpdateTopicDao
from post.service import remove_all_topic_activity
from app.models import Topic
from middleware.response import bad_request, error, success
from rest_framework.views import APIView


class TopicCrudView(APIView):
    @auth_required()
    def topic(self, request):
        attributes = AddTopicDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.error)

        topic = Topic.objects.create(**attributes.data)
        response = {
            'data': TopicDto(topic).data
        }

        return success(response, "topic created successfully", True)

    @auth_required()
    def put(self, request):
        attributes = UpdateTopicDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        topic = Topic.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()

        if not topic:
            return success({}, 'invalid topic', False)

        for attr, value in attributes.data.items():
            setattr(topic, attr, value)
        topic.save()

        response = {
            'data': TopicDto(topic).data
        }
        return success(response, 'topic updated successfully', True)

    @auth_required()
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        topic = Topic.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not topic:
            return success({}, 'invalid uuid', False)

        topic.is_disabled = True
        topic.save()

        remove_all_topic_activity(topic.id)

        return success({}, 'account deleted successfully', True)

    @auth_required()
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        topic = Topic.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not topic:
            return success({}, 'invalid uuid', False)
        
        response = {
            'data': TopicDto(topic).data
        }

        return success(response, 'topic fethced successfully', True)