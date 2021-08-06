from typing import Match
from rest_framework.permissions import BasePermission


def user_type(user):
    if user.is_staff == False and user.is_superuser == False:
        return 'student'

    if user.is_staff == True and user.is_superuser == False:
        return 'facilitator'

    if user.is_staff == True and user.is_superuser == True:
        return 'instructor'


class CoursePermissions(BasePermission):
    def has_permission(self, request, view):
        user = user_type(request.user)

        if request.method == 'GET':
            return True

        if request.method == 'POST' or request.method == 'DELETE':
            return True if user == 'instructor' else False


class EnrollStudentPermissions(BasePermission):
    def has_permission(self, request, view):
        user = user_type(request.user)

        return True if user == 'instructor' else False


class ActivityPermissions(BasePermission):
    def has_permission(self, request, view):
        user = user_type(request.user)

        return True if user == 'facilitator' or user == 'instructor' else False


class SubmissionPermissions(BasePermission):
    def has_permission(self, request, view):
        user = user_type(request.user)

        if request.method == 'POST':
            return True if user == 'student' else False

        if request.method == 'PUT':
            return True if user == 'facilitator' or user == 'instructor' else False
