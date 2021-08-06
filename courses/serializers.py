from rest_framework import serializers
from accounts.serializers import StudentSerializer


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    users = StudentSerializer(many=True, required=False)


class EnrollStutendSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100)
    )


class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    grade = serializers.FloatField()
    repo = serializers.CharField(required=False)
    user_id = serializers.IntegerField(required=False)
    activity_id = serializers.IntegerField(required=False)


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    points = serializers.FloatField()
    submissions = SubmissionSerializer(many=True, required=False)
