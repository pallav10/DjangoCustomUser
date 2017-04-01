from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        # check if valid token has been provided

        return request.user.is_authenticated()


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # check if user is owner
        return request.user.is_authenticated()

