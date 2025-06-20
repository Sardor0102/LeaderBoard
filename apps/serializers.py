from rest_framework.serializers import ModelSerializer

from apps.models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'password', 'phone_number', 'role'



class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = 'name', 'curse_id', 'teacher_id'


class UserGroupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['group']


class GroupTeacherSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['teacher']


class HomeworkSerializer(ModelSerializer):
    class Meta:
        model = HomeWork
        fields = 'title', 'description', 'points', 'start_date', 'deadline', 'line_limit', 'teacher', 'group', 'file_extension', 'ai_grading_prompt'



class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = 'homework', 'student', 'ai_grade', 'final_grade', 'ai_feedback'


