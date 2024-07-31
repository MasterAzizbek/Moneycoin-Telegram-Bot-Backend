from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any user.
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_admin   
    
class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin