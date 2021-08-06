from rest_framework.permissions import BasePermission


class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff == False and request.user.is_superuser == False


class IsFacilitatorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff == True and request.user.is_superuser == False


class IsInstructorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff == True and request.user.is_superuser == True


class CoursePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if request.method == 'POST' or request.method == 'PUT':
            return request.user.is_staff == True and request.user.is_superuser == True


class EnrollStudentPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff == True and request.user.is_superuser == True
