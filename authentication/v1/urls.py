from authentication.v1.views.login import LoginView
from authentication.v1.views.signup import SignUpView
from django.conf.urls import url


urlpatterns = [
    url(r'^signup$', SignUpView.as_view()),
    url(r'^login$', LoginView.as_view()),
]