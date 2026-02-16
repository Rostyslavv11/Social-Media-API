from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response

from .models import UserProfile
from .serializers import (
    UserProfileListSerializer,
    UserProfileRetrieveSerializer,
    UserProfileCreateUpdateSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_serializer_class(self):

        if self.action == "list":
            return UserProfileListSerializer
        if self.action == "retrieve":
            return UserProfileRetrieveSerializer
        if self.action == "update" or self.action == "partial_update" or self.action == "create":
            return UserProfileCreateUpdateSerializer

        return UserProfileListSerializer

    def perform_create(self, serializer):
        if UserProfile.objects.filter(user=self.request.user).exists():
            raise ValidationError({"detail": "Profile already exists for this user."})
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = UserProfile.objects.all()

        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        username = self.request.query_params.get("username")
        bio = self.request.query_params.get("bio")
        location = self.request.query_params.get("location")
        gender = self.request.query_params.get("gender")

        if first_name:
            queryset = queryset.filter(user__first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(user__last_name__icontains=last_name)

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        if bio:
            queryset = queryset.filter(bio__icontains=bio)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if gender:
            queryset = queryset.filter(gender__icontains=gender)

        return queryset

@api_view(["GET"])
def retrieve_my_profile(request):
    if request.method == "GET":
        my_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileRetrieveSerializer(my_profile)
        return Response(serializer.data)

