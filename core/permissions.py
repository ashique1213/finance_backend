from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsAnalystOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['analyst', 'admin']

class IsViewerOrHigher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated