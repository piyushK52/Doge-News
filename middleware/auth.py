from app.models import Session, User
from middleware.response import unauthorized
from django.apps import apps

def auth_required():
    def authenticator(func):
        def wrap(context, request):
            if 'HTTP_AUTHORIZATION' not in request.META:
                return unauthorized({})

            auth_token = request.META['HTTP_AUTHORIZATION']
            auth_token = auth_token.replace('Bearer ', '')

            session = Session.objects.filter(token=auth_token).first()
            if not session:
                return unauthorized({})

            request.user = User.objects.get(uuid=session.user_uuid)
            request.token = auth_token
            return func(context, request)
        wrap.__name__ = func.__name__
        return wrap
    return authenticator