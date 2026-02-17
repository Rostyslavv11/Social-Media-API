from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User, UserProfile
from posts.models import Comment, Post


class PostApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="pass1234",
            username="owner",
        )
        self.followed_user = User.objects.create_user(
            email="followed@example.com",
            password="pass1234",
            username="followed",
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="pass1234",
            username="other",
        )

        self.user_profile = UserProfile.objects.create(user=self.user)
        UserProfile.objects.create(user=self.followed_user)
        UserProfile.objects.create(user=self.other_user)
        self.user_profile.following.add(self.followed_user)

        self.client.force_authenticate(self.user)

    def test_create_post(self):
        payload = {"content": "Hello #Django"}

        response = self.client.post("/api/posts/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)
        self.assertEqual(response.data["hashtag_list"], ["django"])

    def test_get_my_posts(self):
        own_post = Post.objects.create(author=self.user, content="My post")
        Post.objects.create(author=self.followed_user, content="Not mine")

        response = self.client.get("/api/posts/my/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], own_post.id)

    def test_get_feed_posts(self):
        own_post = Post.objects.create(author=self.user, content="Owner post")
        followed_post = Post.objects.create(author=self.followed_user, content="Followed post")
        Post.objects.create(author=self.other_user, content="Other post")

        response = self.client.get("/api/posts/feed/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item["id"] for item in response.data}
        self.assertEqual(returned_ids, {own_post.id, followed_post.id})

    def test_filter_by_hashtag(self):
        matched = Post.objects.create(author=self.user, content="This is #Python")
        Post.objects.create(author=self.user, content="No tag here")

        response = self.client.get("/api/posts/?hashtag=python")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], matched.id)

    def test_like_and_unlike_post(self):
        post = Post.objects.create(author=self.followed_user, content="Like me")

        like_response = self.client.post(f"/api/posts/{post.id}/like/")
        unlike_response = self.client.post(f"/api/posts/{post.id}/unlike/")

        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unlike_response.data["likes_count"], 0)

    def test_user_cannot_update_other_user_post(self):
        post = Post.objects.create(author=self.followed_user, content="Protected post")

        response = self.client.patch(f"/api/posts/{post.id}/", {"content": "Hacked"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        post.refresh_from_db()
        self.assertEqual(post.content, "Protected post")

    def test_user_can_update_own_comment_and_cannot_update_other_comment(self):
        post = Post.objects.create(author=self.followed_user, content="Post")
        own_comment = Comment.objects.create(post=post, author=self.user, content="My comment")
        other_comment = Comment.objects.create(post=post, author=self.followed_user, content="Their comment")

        own_response = self.client.patch(
            f"/api/posts/comments/{own_comment.id}/",
            {"content": "Updated my comment"},
            format="json",
        )
        other_response = self.client.patch(
            f"/api/posts/comments/{other_comment.id}/",
            {"content": "Should fail"},
            format="json",
        )

        self.assertEqual(own_response.status_code, status.HTTP_200_OK)
        self.assertEqual(other_response.status_code, status.HTTP_403_FORBIDDEN)
