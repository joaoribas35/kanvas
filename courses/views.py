from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth.models import User
from courses.models import Course, Activity, Submission
from courses.serializers import CourseSerializer, EnrollStutendSerializer, ActivitySerializer, SubmissionSerializer
from courses.permissions import CoursePermissions, EnrollStudentPermissions, ActivityPermissions, SubmissionPermissions
from rest_framework.permissions import IsAuthenticated


class CourseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [CoursePermissions]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        course = Course.objects.get_or_create(**validated_data)[0]

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseDetailView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [CoursePermissions]

    def get(self, request, course_id=''):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, course_id=''):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND)

        course.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivityView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ActivityPermissions]

    def get(self, request):
        activity = Activity.objects.all()
        serializer = ActivitySerializer(activity, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        activity = Activity.objects.get_or_create(**validated_data)[0]

        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubmitActivityView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [SubmissionPermissions]

    def post(self, request, activity_id=''):
        serializer = SubmissionSerializer(data=request.data)
        user = request.user

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        try:
            activity = Activity.objects.get(id=activity_id)
        except Activity.DoesNotExist:
            return Response({"errors": "invalid activity_id"}, status=status.HTTP_404_NOT_FOUND)

        submission = Submission.objects.create(
            repo=validated_data['repo'], user=user, activity=activity)

        serializer = SubmissionSerializer(submission)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubmissionDetailView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [SubmissionPermissions]

    def put(self, request, submission_id=''):
        serializer = SubmissionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return Response({"errors": "invalid submission_id"}, status=status.HTTP_404_NOT_FOUND)

        submission.grade = validated_data['grade']
        submission.save()

        serializer = SubmissionSerializer(submission)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmissionView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        student = True if user.is_staff == False and user.is_superuser == False else False

        if student:
            submissions = Submission.objects.filter(user_id=user.id)
            serializer = SubmissionSerializer(submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
