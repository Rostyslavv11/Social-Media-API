# Social-Media-API

DRF API with JWT authentication for profiles, posts, likes, comments, and follow/unfollow.

## Auth

1. Get tokens:
```http
POST /api/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

2. Refresh token:
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

Use access token in all protected requests:
`Authorization: Bearer <access_token>`

## Permissions Summary

- All API endpoints require authentication.
- Users can update/delete only their own profile.
- Users can update/delete only their own posts.
- Users can update/delete only their own comments.
- Follow/unfollow and like/unlike are available only for authenticated users.

## Accounts Endpoints

- `GET /api/accounts/user-profiles/` list profiles (supports filters: `first_name`, `last_name`, `username`, `bio`, `location`, `gender`)
- `POST /api/accounts/user-profiles/` create own profile
- `GET /api/accounts/user-profiles/{id}/` retrieve profile
- `PATCH /api/accounts/user-profiles/{id}/` update own profile only
- `DELETE /api/accounts/user-profiles/{id}/` delete own profile only
- `POST /api/accounts/user-profiles/{id}/follow/` follow user
- `POST /api/accounts/user-profiles/{id}/unfollow/` unfollow user
- `GET /api/accounts/me/` retrieve own profile
- `PATCH /api/accounts/me/` update own profile
- `DELETE /api/accounts/me/` delete own profile
- `GET /api/accounts/my_following/` list profiles you follow
- `GET /api/accounts/my_followers/` list your followers

## Posts Endpoints

- `GET /api/posts/` list posts
- `POST /api/posts/` create post (`content`, optional `media`)
- `PATCH /api/posts/{id}/` update own post only
- `DELETE /api/posts/{id}/` delete own post only
- `GET /api/posts/my/` list own posts
- `GET /api/posts/feed/` list own posts + users you follow
- `POST /api/posts/{id}/like/` like post
- `POST /api/posts/{id}/unlike/` unlike post

### Post filters

- `hashtag=python`
- `author=john`
- `user_id=2`
- `search=django`
- `created_from=2026-02-01`
- `created_to=2026-02-17`

Example:
`GET /api/posts/?hashtag=python&created_from=2026-02-01`

## Comments Endpoints

- `GET /api/posts/comments/` list comments
- `GET /api/posts/comments/?post_id={post_id}` list comments for one post
- `POST /api/posts/comments/` create comment
- `PATCH /api/posts/comments/{id}/` update own comment only
- `DELETE /api/posts/comments/{id}/` delete own comment only

Create comment example:
```http
POST /api/posts/comments/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "post": 1,
  "content": "Nice post!"
}
```

## Sample Responses

Post create response:
```json
{
  "id": 10,
  "author": 1,
  "author_username": "user1",
  "content": "Learning DRF #django",
  "media": null,
  "likes_count": 0,
  "is_liked": false,
  "hashtag_list": ["django"],
  "created_at": "2026-02-17T19:00:00Z",
  "updated_at": "2026-02-17T19:00:00Z"
}
```

Comment create response:
```json
{
  "id": 3,
  "post": 10,
  "author": 1,
  "author_username": "user1",
  "content": "Nice post!",
  "created_at": "2026-02-17T19:05:00Z",
  "updated_at": "2026-02-17T19:05:00Z"
}
```

## Run With Docker

1. Create environment file:
```bash
cp .env.example .env
```
PowerShell alternative:
```powershell
Copy-Item .env.example .env
```

2. Ensure `.env` has a valid `SECRET_KEY` value.

3. Build and start:
```bash
docker compose up --build
```

4. API will be available at:
`http://localhost:8000/`

Notes:
- Migrations run automatically on container start.
- Source code is mounted into the container for development.
