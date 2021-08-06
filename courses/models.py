from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)


class Activity(models.Model):
    title = models.CharField(max_length=255)
    points = models.FloatField()


class Submission(models.Model):
    grade = models.FloatField(null=True)
    repo = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=CASCADE)
    activity = models.ForeignKey(
        Activity, on_delete=CASCADE, related_name="submissions")
