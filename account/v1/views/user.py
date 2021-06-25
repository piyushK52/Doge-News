from middleware.auth import auth_required
from account.service import remove_all_user_activity
from account.v1.serializers.dto import UserDto
from app.models import UserProfile
from middleware.response import bad_request, error, success
from account.v1.serializers.dao import AddUserDao, UUIDDao, UpdateUserDao
from rest_framework.views import APIView


class UserCrudView(APIView):
    @auth_required()
    def post(self, request):
        attributes = AddUserDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.error)

        user = UserProfile.objects.create(**attributes.data)
        response = {
            'data': UserDto(user).data
        }

        return success(response, "user created successfully", True)

    @auth_required()
    def put(self, request):
        attributes = UpdateUserDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = UserProfile.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()

        if not user:
            return success({}, 'invalid user', False)

        for attr, value in attributes.data.items():
            setattr(user, attr, value)
        user.save()

        response = {
            'data': UserDto(user).data
        }
        return success(response, 'user updated successfully', True)

    @auth_required()
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = UserProfile.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not user:
            return success({}, 'invalid uuid', False)

        user.is_disabled = True
        user.save()

        remove_all_user_activity(user.id)

        return success({}, 'account deleted successfully', True)

    @auth_required()
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = UserProfile.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not user:
            return success({}, 'invalid uuid', False)
        
        response = {
            'data': UserDto(user).data
        }

        return success(response, 'user fethced successfully', True)

        
        