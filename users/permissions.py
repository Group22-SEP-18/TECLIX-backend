from rest_framework import permissions


class IsSalesperson(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'SALESPERSON'

    def has_object_permission(self, request, view, obj):
        return request.user.user_role == 'SALESPERSON'


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.user_role == 'MANAGER'

    def has_object_permission(self, request, view, obj):
        return request.user.user_role == 'MANAGER'


class IsOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'OFFICER'

    def has_object_permission(self, request, view, obj):
        return request.user.user_role == 'OFFICER'
