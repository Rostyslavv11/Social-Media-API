from django.urls import path, include
from rest_framework import routers

from accounts import views
from accounts.views import get_following, get_followers, ManageUserView

router = routers.DefaultRouter()
router.register("user-profiles", views.UserProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("me/", ManageUserView.as_view(), name="my-profile"),
    path("my_following/", get_following, name="following"),
    path("my_followers/", get_followers, name="followers"),
]

app_name = "accounts"