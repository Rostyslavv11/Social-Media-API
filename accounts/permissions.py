from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProfileOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if getattr(view, "action", None) in {"follow", "unfollow"} and request.method == "POST":
            return request.user.is_authenticated
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
