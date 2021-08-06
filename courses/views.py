from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from courses.models import Course
from django.contrib.auth.models import User
from courses.serializers import CourseSerializer, EnrollStutendSerializer
from courses.permissions import CoursePermissions, EnrollStudentPermissions

import ipdb


class CourseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [CoursePermissions]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        user = request.user

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        course = Course.objects.get_or_create(**validated_data)[0]

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EnrollStudentView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [EnrollStudentPermissions]

    def put(self, request, course_id=''):
        serializer = EnrollStutendSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        students = list()
        for user_id in validated_data['user_ids']:

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"errors": "invalid user_id list"}, status=status.HTTP_404_NOT_FOUND)

            if user.is_staff == False and user.is_superuser == False:
                students.append(user)
            else:
                return Response({"errors": "Only students can be enrolled in the course."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND)

        course.users.set(students)
        serializer = CourseSerializer(course)

        return Response(serializer.data)
