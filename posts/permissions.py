from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if getattr(view, "action", None) in {"like", "unlike"} and request.method == "POST":
            return request.user.is_authenticated
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
