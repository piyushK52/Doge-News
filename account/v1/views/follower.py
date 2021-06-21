from middleware.auth import auth_required
from account.v1.serializers.dto import RelationshipDto, UserDto
from app.models import Relationship, User
from middleware.response import bad_request, success
from rest_framework.views import APIView
from account.v1.serializers.dao import UUIDDao

class FollowerView(APIView):

    # for following someone
    @auth_required()
    def post(self, request):
        attributes = UUIDDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        relation = Relationship.objects.filter(follower_user_uuid=request.user.uuid, followed_user_uuid=attributes.data['uuid']).first()

        if relation:
            return success({}, 'relationship already exists', True)

        
        relation = Relationship.objects.create({'follower_user_uuid': request.user.uuid, 'followed_user_uuid': attributes.data['uuid']})

        response = {
            'data': RelationshipDto(relation).data
        }

        return success({}, 'follower added successfully', True)


    # for un-following someone
    @auth_required()
    def delete(self, request):
        attributes = UUIDDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        relation = Relationship.objects.filter(follower_user_uuid=request.user.uuid, followed_user_uuid=attributes.data['uuid']).first()

        if not relation:
            return success({}, 'invalid uuid', True)

        relation.delete()

        return success({}, 'follower removed successfully', True)


    # for fetching follower count of a particular user
    @auth_required()
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        follower_count = Relationship.objects.filter(followed_user_uuid=attributes.data['uuid']).all().count()
        user = User.objects.filter(uuid=attributes.data['uuid']).first()

        response = {
            'data': {
                'user': UserDto(user).data,
                'follower_count': follower_count
            }
        }

        return success(response, 'follower count fetched successfully', True)