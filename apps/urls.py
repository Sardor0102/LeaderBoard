from django.urls import path

from apps.views import *

urlpatterns = [
    path("admin/teachers", TeachersAPIView.as_view()),

    path("admin/teacher/<int:pk>", TeacherAPIView.as_view()),

    path("admin/students", StudentsAPIView.as_view()),

    path("admin/student/<int:pk>", StudentAPIView.as_view()),

    path("admin/groups", GroupsAPIView.as_view()),

    path("admin/group/<int:pk>", GroupAPIView.as_view()),

    path("admin/students/<int:pk>/group", StudentGroupUpdateAPIView.as_view()),

    path("admin/group/<int:pk>/teacher", GroupTeacherUpdateAPIView.as_view()),

    path("admin/group/<int:pk>/leaderboard", GroupLeaderBoard.as_view()),

    path("teacher/homeworks", HomeworksAPIView.as_view()),

    path("teacher/homework/<int:pk>", HomeworkAPIView.as_view()),

    path("teacher/groups", TeacherGroupAPIView.as_view()),

    path("teacher/groups/<int:pk>/submissions", TeacherGroupSubmissionAPIView.as_view()),

    path("teacher/groups/<int:pk>/leaderboard", TeacherGroupLeaderboardAPIView.as_view()),

    path("student/leaderboard", StudentLeaderboardAPIView.as_view()),

    path("student/homeworks", StudentHomeworkAPIView.as_view()),

    path("student/homework/<int:pk>/submit", StudentHomeworkSubmitAPIView.as_view())
]
