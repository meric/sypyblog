from rest_framework.permissions import *


def Or(*args):
    """
    The `ViewSet`'s permission_classes are ANDed together. There are times an
    OR might be useful. This method implements the OR operator for
    permission_classes.
    """
    class Permission(BasePermission):
        """
        One of the permission classes in `args` evaluates to True.
        """
        def has_permission(self, request, view):
            for permission in self.get_permissions():
                if permission.has_permission(request, view):
                    return True
            return False

        def has_object_permission(self, request, view, obj):
            for permission in self.get_permissions():
                if permission.has_permission(request, view):
                    if permission.has_object_permission(request, view, obj):
                        return True
            return False

        def get_permissions(self):
            return (permission() for permission in args)

    return Permission


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.is_staff


class IsReadOnly(BasePermission):

    """
    The request is a read-only request.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsCreateOnly(BasePermission):

    """
    The request is a create-only request.
    """

    def has_permission(self, request, view):
        return request.method not in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in ['POST'] or obj is None


class IsAuthor(BasePermission):
    """
    The object's `author` attribute is the authenticated user.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated() and obj.author == request.user

