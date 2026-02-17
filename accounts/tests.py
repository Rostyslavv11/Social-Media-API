from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User, UserProfile


class AccountApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user1@example.com", password="pass1234", username="user1")
        self.other_user = User.objects.create_user(
            email="user2@example.com",
            password="pass1234",
            username="user2",
        )
        self.user_profile = UserProfile.objects.create(user=self.user, bio="bio1")
        self.other_profile = UserProfile.objects.create(user=self.other_user, bio="bio2")
        self.client.force_authenticate(self.user)

    def test_user_cannot_update_other_profile(self):
        response = self.client.patch(
            f"/api/accounts/user-profiles/{self.other_profile.id}/",
            {"bio": "hacked"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_follow_and_unfollow(self):
        follow_response = self.client.post(f"/api/accounts/user-profiles/{self.other_profile.id}/follow/")
        unfollow_response = self.client.post(f"/api/accounts/user-profiles/{self.other_profile.id}/unfollow/")

        self.assertEqual(follow_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unfollow_response.status_code, status.HTTP_200_OK)
