from account.v1.serializers.dto import UserDto
from util.hash import PBKDF2PasswordHasher
from authentication.v1.serializers.dao import UserLoginDao
from rest_framework.views import APIView
from middleware.response import success, bad_request
from app.models import Session, UserProfile

class LoginView(APIView):
    def post(self, request):
        attributes = UserLoginDao(data=request.data)

        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = UserProfile.objects.filter(email=attributes.data['email'], is_disabled=False).first()
        if not user:
            return success({}, "invalid username or password", False)

        password = PBKDF2PasswordHasher().encode(attributes.data['password'])
        if user.password != password:
            return success({}, 'invalid username or password', False)

        session = Session.objects.filter(user=user, is_disabled=False).first()
        if session:
            session.delete()
        session = Session.objects.create(user_id=user.id)

        response = {
            'token': session.token,
            'user': UserDto(user).data
        }

        return success(response, "user logged in successfully", True)