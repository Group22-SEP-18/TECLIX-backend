from rest_framework import permissions


class IsSalesperson(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user.user_role)

        return request.user.user_role == 'SALESPERSON'


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user.user_role)

        return request.user.user_role == 'MANAGER'


class IsOfficer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user.user_role)
        return request.user.user_role == 'OFFICER'
