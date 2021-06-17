from app.models import Session
from django.http import HttpResponse

class CustomTokenAuthentication(object):

    def process_request(self, request):
        access_token = request.META.get('TOKEN', '')
        if Session.objects.filter(token=access_token).exists():
            return None
        else:
            # return None
            res =  HttpResponse("Invalid token", status=401)
            res["WWW-Authenticate"] = "Invalid Token"
            return res