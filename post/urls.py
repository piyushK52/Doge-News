from post.v1.views.comment import CommentCrudView, CommentListView
from post.v1.views.vote import VoteCrudView
from post.v1.views.topic import TopicCrudView
from post.v1.views.post import PostCrudView, PostListView
from django.conf.urls import url


urlpatterns = [
    url(r'^post$', PostCrudView.as_view()),
    url(r'^post/list$', PostListView.as_view()),
    url(r'^topic$', TopicCrudView.as_view()),
    url(r'^comment$', CommentCrudView.as_view()),
    url(r'^comment/list$', CommentListView.as_view()),
]