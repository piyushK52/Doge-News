from account.v1.views.follower import FollowerView
from account.v1.views.user import UserCrudView
from django.conf.urls import url

urlpatterns = [
    url(r'^user$', UserCrudView.as_view()),
    url(r'^follower$', FollowerView.as_view()),
]