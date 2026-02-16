from rest_framework import serializers

from accounts.models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user",
                  "profile_picture",
                  "bio",
                  "date_of_birth",
                  "location",
                  "gender"
        )
        read_only_fields = ("user",
                  "profile_picture",
                  "bio",
                  "date_of_birth",
                  "location",
                  "gender"
        )


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ("user", "profile_picture", "bio", "date_of_birth", "location", "gender")


class UserProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user",
                  "profile_picture",
                  "bio",
                  "date_of_birth",
                  "location",
                  "gender"
        )
        read_only_fields = ("user",)