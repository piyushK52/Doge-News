from middleware.auth import auth_required
from account.v1.serializers.dto import RelationshipDto, UserDto
from app.models import Relationship, UserProfile
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

        user = UserProfile.objects.filter(uuid=attributes.data['uuid']).first()
        if not user:
            return success({}, 'invalid uuid', True)

        if user.id == request.user_id:
            return success({}, 'cannot follow self', True)
        
        relation = Relationship.objects.filter(follower_user_id=request.user_id, followed_user_id=user.id).first()

        if relation:
            return success({}, 'already following', True)

        print("printing relationship obj", request.user.id, user.id)
        relation = Relationship.objects.create(follower_user_id=request.user_id, followed_user_id=user.id)

        response = {
            'data': RelationshipDto(relation).data
        }

        return success(response, 'follower added successfully', True)


    # for un-following someone
    @auth_required()
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = UserProfile.objects.filter(uuid=attributes.data['uuid']).first()
        if not user:
            return success({}, 'invalid uuid', True)

        if user.id == request.user_id:
            return success({}, 'operation not allowed on self', True)

        relation = Relationship.objects.filter(follower_user_id=request.user_id, followed_user_id=user.id).first()

        if not relation:
            return success({}, 'follower absent', True)

        relation.delete()

        return success({}, 'follower removed successfully', True)


    # for fetching follower count of a particular user
    @auth_required()
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = UserProfile.objects.filter(uuid=attributes.data['uuid']).first()
        if not user:
            return success({}, 'invalid uuid', True)
        
        follower_count = Relationship.objects.filter(followed_user_id=user.id).all().count()

        response = {
            'data': {
                'user': UserDto(user).data,
                'follower_count': follower_count
            }
        }

        return success(response, 'follower count fetched successfully', True)