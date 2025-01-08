from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
SAFE_METHODS_AND_PUT = ('GET', 'PUT', 'HEAD', 'OPTIONS')


class IsAdminAndOwnerOrReadOnly(BasePermission):
    def is_owner(self, request, obj):
        owner = None
        try:
            owner = obj.user
        except Exception:
            return False
        return request.user == owner

    def additional_condition(self, request):
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or self.is_owner(request, obj)

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS_AND_PUT or self.additional_condition(request):
            return True
        return request.user.is_staff


class IsPosterAdminAndOwnerOrReadOnly(IsAdminAndOwnerOrReadOnly):
    def additional_condition(self, request):
        return request.user.is_authenticated


class IsAdminOrReadOnly(IsAdminAndOwnerOrReadOnly):
    def is_owner(self, request, obj):
        return False
