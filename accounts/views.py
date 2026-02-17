from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .permissions import IsProfileOwnerOrReadOnly
from .serializers import (
    UserProfileListSerializer,
    UserProfileRetrieveSerializer,
    UserProfileCreateSerializer, UserProfileUpdateSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = (IsAuthenticated, IsProfileOwnerOrReadOnly)

    def get_serializer_class(self):

        if self.action == "list":
            return UserProfileListSerializer
        if self.action == "retrieve":
            return UserProfileRetrieveSerializer
        if self.action == "update" or self.action == "partial_update":
            return UserProfileUpdateSerializer
        if self.action == "create":
            return UserProfileCreateSerializer

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

    @action(detail=True, methods=["post"], url_path="follow")
    def follow(self, request, pk=None):
        target_profile = self.get_object()
        current_profile = request.user.userprofile

        if target_profile.user == request.user:
            raise ValidationError({"detail": "You cannot follow yourself."})

        current_profile.following.add(target_profile.user)
        target_profile.followers.add(request.user)

        return Response({"detail": f"You are now following {target_profile.user.username}."})

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow(self, request, pk=None):
        target_profile = self.get_object()
        current_profile = request.user.userprofile

        current_profile.following.remove(target_profile.user)
        target_profile.followers.remove(request.user)

        return Response({"detail": f"You unfollowed {target_profile.user.username}."})


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

@api_view(["GET"])
def get_following(request):
    profile = request.user.userprofile
    following = UserProfile.objects.filter(user__in=profile.following.all())
    serializer = UserProfileListSerializer(following, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_followers(request):
    profile = request.user.userprofile
    followers = UserProfile.objects.filter(user__in=profile.followers.all())
    serializer = UserProfileListSerializer(followers, many=True)
    return Response(serializer.data)
