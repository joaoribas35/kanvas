from django.urls import path

from courses.views import CourseView, EnrollStudentView

urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/<int:course_id>/registrations/', EnrollStudentView.as_view()),
]
