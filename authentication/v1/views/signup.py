from account.v1.serializers.dto import UserDto
from app.models import UserProfile
from authentication.v1.serializers.dao import UserSignUpDao
from rest_framework.views import APIView
from middleware.response import success, bad_request

class SignUpView(APIView):
    def post(self, request):
        print("request--> ", request.data)
        attributes = UserSignUpDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.errors)
        print("data--> ", attributes.data)

        user = UserProfile.objects.filter(email=attributes.validated_data['email'], is_disabled=False).first()

        if user:
            return success({}, "UserProfile already exists", False)

        user = UserProfile.objects.create(**attributes.data)

        response = {
            'data': UserDto(user).data
        }

        return success(response, "user created successfully", True)
