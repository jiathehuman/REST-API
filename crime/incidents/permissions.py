# Reference: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
from rest_framework import permissions

class ReadOnlyOrIsOwner(permissions.BasePermission):
    """
    Permission to allow only owners to edit an object
    """
    def has_object_permission(self, request, view, obj):
        # read permissions allowed to all requests, always allow GET HEAD OR OPTIONS
        # SAFE_METHODS contains such methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # give write permissions to owner of incidents
        return obj.owner == request.user