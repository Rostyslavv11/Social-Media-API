from rest_framework import serializers

from accounts.models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class UserProfileListSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "profile_picture",
            "bio",
            "date_of_birth",
            "location",
            "gender",
            "followers",
            "following",
        )
        read_only_fields = (
            "id",
            "user",
            "followers",
            "following",
        )


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "profile_picture",
            "bio",
            "date_of_birth",
            "location",
            "gender",
            "followers",
            "following",
        )
        read_only_fields = ("id", "user", "followers", "following")


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "profile_picture",
            "bio",
            "date_of_birth",
            "location",
            "gender",
            "followers",
            "following",
        )
        read_only_fields = ("id", "user", "followers", "following")


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "profile_picture",
            "bio",
            "date_of_birth",
            "location",
            "gender",
            "followers",
            "following",
        )
        read_only_fields = ("id", "user", "followers", "following")
