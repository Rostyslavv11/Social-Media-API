from django.urls import path, include
from rest_framework import routers

from accounts import views
from accounts.views import retrieve_my_profile

router = routers.DefaultRouter()
router.register("user-profiles", views.UserProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("me/", retrieve_my_profile, name="my-profile"),
]

app_name = "accounts"