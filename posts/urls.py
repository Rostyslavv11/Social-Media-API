from django.urls import include, path
from rest_framework import routers

from posts.views import CommentViewSet, PostViewSet

post_router = routers.DefaultRouter()
post_router.register("", PostViewSet, basename="posts")

comment_router = routers.DefaultRouter()
comment_router.register("", CommentViewSet, basename="comments")

urlpatterns = [
    path("comments/", include(comment_router.urls)),
    path("", include(post_router.urls)),
]
