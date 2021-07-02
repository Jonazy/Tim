from rest_framework import permissions


class IsHost(permissions.BasePermission):
    def has_object_permission(self, request, views, obj):
        return obj.host == request.user