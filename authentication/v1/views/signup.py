from account.v1.serializers.dto import UserDto
from app.models import User
from authentication.v1.serializers.dao import UserSignUpDao
from rest_framework.views import APIView
from middleware.response import success, bad_request

class SignUpView(APIView):
    def post(self, request):
        attributes = UserSignUpDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = User.objects.filter(email=attributes.validated_data['email'], is_disabled=False).first()

        if user:
            return success({}, "User already exists", False)

        user = User.objects.create(**attributes.data)

        response = {
            'data': UserDto(user)
        }

        return success(response, "user created successfully", True)
