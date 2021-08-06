from django.urls import path

from courses.views import CourseView, CourseDetailView, EnrollStudentView, ActivityView, SubmitActivityView, SubmissionDetailView, SubmissionView

urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/<int:course_id>/', CourseDetailView.as_view()),
    path('courses/<int:course_id>/registrations/', EnrollStudentView.as_view()),
    path('activities/', ActivityView.as_view()),
    path('activities/<int:activity_id>/submissions/',
         SubmitActivityView.as_view()),
    path('submissions/<int:submission_id>/', SubmissionDetailView.as_view()),
    path('submissions/', SubmissionView.as_view()),
]
