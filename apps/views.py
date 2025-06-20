from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.serializers import *


# Create your views here.
class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsAdminOrTeacherRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'teacher']


class TeachersAPIView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Admin: teacher"])
    def get(self, request):
        objects = User.objects.filter(role="teacher")
        serializer = UserSerializer(instance=objects, many=True)
        return Response(serializer.data)

    @extend_schema(request=UserSerializer, tags=["Admin: teacher"])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj = User.objects.filter(email=request.data.get("email")).first()
            return JsonResponse({"message": "User created successfully.", "status": "201", "user_id": obj.id})
        return JsonResponse({"message": "There was an error creating the user.", "status": "500"})


class TeacherAPIView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Admin: teacher"])
    def get(self, request, pk):
        objects = User.objects.filter(pk=pk, role="teacher")
        if objects.exists():
            serializer = UserSerializer(instance=objects.first())
            return Response(serializer.data)
        return JsonResponse({"message": "No teacher with such pk was found", "status": "404"})


    @extend_schema(request=UserSerializer, tags=["Admin: teacher"])
    def put(self, request, pk):
        obj = User.objects.filter(pk=pk, role="teacher")
        if obj.exists():
            for key, value in request.data.items():
                if value:
                    obj.update(**{key: value})
            serializer = UserSerializer(instance=obj.first())
            return Response(serializer.data)
        else:
            return JsonResponse({"message": "No teacher with such pk was found", "status": "404"})


    @extend_schema(tags=["Admin: teacher"])
    def delete(self, request, pk):
        obj = User.objects.filter(pk=pk, role="teacher")
        if obj.exists():
            obj = obj.first()
            serializer = UserSerializer(instance=obj)
            data = serializer.data
            obj.delete()
            return JsonResponse({"message": "Teacher successfully deleted.", "status": "200", "user": data})
        return JsonResponse({"message": "No teacher with such pk was found", "status": "404"})



class StudentsAPIView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Admin: student"])
    def get(self, request):
        objects = User.objects.filter(role="student")
        serializer = UserSerializer(instance=objects, many=True)
        return Response(serializer.data)

    @extend_schema(request=UserSerializer, tags=["Admin: student"])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj = User.objects.filter(email=request.data.get("email")).first()
            return JsonResponse({"message": "User created successfully.", "status": "201", "user_id": obj.id})
        return JsonResponse({"message": "There was an error creating the user.", "status": "500"})


class StudentAPIView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Admin: student"])
    def get(self, request, pk):
        objects = User.objects.filter(pk=pk, role="student")
        if objects.exists():
            serializer = UserSerializer(instance=objects.first())
            return Response(serializer.data)
        return JsonResponse({"message": "No student with such pk was found", "status": "404"})


    @extend_schema(request=UserSerializer, tags=["Admin: student"])
    def put(self, request, pk):
        obj = User.objects.filter(pk=pk, role="student")
        if obj.exists():
            for key, value in request.data.items():
                if value:
                    obj.update(**{key: value})
            serializer = UserSerializer(instance=obj.first())
            return Response(serializer.data)
        else:
            return JsonResponse({"message": "No student with such pk was found", "status": "404"})


    @extend_schema(tags=["Admin: student"])
    def delete(self, request, pk):
        obj = User.objects.filter(pk=pk, role="student")
        if obj.exists():
            obj = obj.first()
            serializer = UserSerializer(instance=obj)
            data = serializer.data
            obj.delete()
            return JsonResponse({"message": "Student successfully deleted.", "status": "200", "user": data})
        return JsonResponse({"message": "No student with such pk was found", "status": "404"})



class GroupsAPIView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Admin: group"])
    def get(self, request):
        objects = Group.objects.all()
        serializer = GroupSerializer(instance=objects, many=True)
        return Response(serializer.data)

    @extend_schema(request=GroupSerializer, tags=["Admin: group"])
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj = Group.objects.filter(name=request.data.get("name")).first()
            return JsonResponse({"message": "Group created successfully.", "status": "201", "group_id": obj.id})
        return JsonResponse({"message": "There was an error creating the group.", "status": "500"})


class GroupAPIView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Admin: group"])
    def get(self, request, pk):
        objects = Group.objects.filter(pk=pk)
        if objects.exists():
            serializer = GroupSerializer(instance=objects.first())
            return Response(serializer.data)
        return JsonResponse({"message": "No group with such pk was found", "status": "404"})


    @extend_schema(request=GroupSerializer, tags=["Admin: group"])
    def put(self, request, pk):
        obj = Group.objects.filter(pk=pk)
        if obj.exists():
            for key, value in request.data.items():
                if value:
                    obj.update(**{key: value})
            serializer = GroupSerializer(instance=obj.first())
            return Response(serializer.data)
        else:
            return JsonResponse({"message": "No group with such pk was found", "status": "404"})


    @extend_schema(tags=["Admin: group"])
    def delete(self, request, pk):
        obj = Group.objects.filter(pk=pk)
        if obj.exists():
            obj = obj.first()
            serializer = GroupSerializer(instance=obj)
            data = serializer.data
            obj.delete()
            return JsonResponse({"message": "Group successfully deleted.", "status": "200", "group": data})
        return JsonResponse({"message": "No group with such pk was found", "status": "404"})



class StudentGroupUpdateAPIView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(request=UserGroupSerializer, tags=["Admin: other"])
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk, role="student")
        serializer = UserGroupSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupTeacherUpdateAPIView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(request=GroupTeacherSerializer, tags=["Admin: other"])
    def patch(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupTeacherSerializer(instance=group, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupLeaderBoard(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Admin: other"], description="Group leaderboard")
    def get(self, request, pk):
        obj = User.objects.filter(role="student", group_id=pk).order_by('submissions__grades__final_total')
        serializer = UserSerializer(instance=obj, many=True)
        return Response(serializer.data)



#HomeWork
class HomeworksAPIView(APIView):
    permission_classes = [IsAdminOrTeacherRole]

    @extend_schema(tags=["Teacher: homework"])
    def get(self, request):
        objects = HomeWork.objects.all()
        serializer = HomeworkSerializer(instance=objects, many=True)
        return Response(serializer.data)

    @extend_schema(request=HomeworkSerializer, tags=["Teacher: homework"])
    def post(self, request):
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Homework created successfully.", "status": "201", "homework": request.data})
        return JsonResponse({"message": "There was an error creating the homework.", "status": "500"})


class HomeworkAPIView(APIView):
    permission_classes = [IsAdminOrTeacherRole]

    @extend_schema(tags=["Teacher: homework"])
    def get(self, request, pk):
        objects = HomeWork.objects.filter(pk=pk)
        if objects.exists():
            serializer = HomeworkSerializer(instance=objects.first())
            return Response(serializer.data)
        return JsonResponse({"message": "No homework with such pk was found", "status": "404"})


    @extend_schema(request=HomeworkSerializer, tags=["Teacher: homework"])
    def put(self, request, pk):
        obj = HomeWork.objects.filter(pk=pk)
        if obj.exists():
            for key, value in request.data.items():
                if value:
                    obj.update(**{key: value})
            serializer = HomeworkSerializer(instance=obj.first())
            return Response(serializer.data)
        else:
            return JsonResponse({"message": "No homework with such pk was found", "status": "404"})


    @extend_schema(tags=["Teacher: homework"])
    def delete(self, request, pk):
        obj = HomeWork.objects.filter(pk=pk)
        if obj.exists():
            obj = obj.first()
            serializer = HomeworkSerializer(instance=obj)
            data = serializer.data
            obj.delete()
            return JsonResponse({"message": "Homework successfully deleted.", "status": "200", "homework": data})
        return JsonResponse({"message": "No homework with such pk was found", "status": "404"})


# Teacher other:
class TeacherGroupAPIView(APIView):
    permission_classes = [IsAdminOrTeacherRole]

    @extend_schema(tags=["Teacher: other"])
    def get(self, request):
        teacher_id = request.user.id
        groups = Group.objects.filter(teacher_id=teacher_id)
        if groups.exists():
            serializer = GroupSerializer(instance=groups, many=True)
            return JsonResponse({"message": "Groups were found", "status": "200", "data": serializer.data})
        return JsonResponse({"message": "Groups not found", "status": "404"})


class TeacherGroupSubmissionAPIView(APIView):
    permission_classes = [IsAdminOrTeacherRole]

    @extend_schema(tags=["Teacher: other"])
    def get(self, request, pk):
        submissions = Submission.objects.filter(student__group_id=pk)
        if submissions.exists():
            serializer = SubmissionSerializer(instance=submissions, many=True)
            return JsonResponse({"message": "Submissions were found", "status": "200", "data": serializer.data})
        return JsonResponse({"message": "Submissions not found", "status": "404"})


class TeacherGroupLeaderboardAPIView(APIView):
    permission_classes = [IsAdminOrTeacherRole]

    @extend_schema(tags=["Teacher: other"])
    def get(self, request, pk):
        students = User.objects.filter(role="student", group_id=pk).order_by("submissions__grades__final_total")
        if students.exists():
            serializer = UserSerializer(instance=students, many=True)
            return JsonResponse({"message": "Students were found", "status": "200", "data": serializer.data})
        return JsonResponse({"message": "Students not found", "status": "404"})


# Student api:
class StudentLeaderboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Student: api"])
    def get(self, request):
        students = User.objects.filter(role="student", group_id=request.user.group_id).order_by("submissions__grades__final_total")
        if students.exists():
            serializer = UserSerializer(instance=students, many=True)
            return JsonResponse({"message": "Students were found", "status": "200", "data": serializer.data})
        return JsonResponse({"message": "Students not found", "status": "404"})


class StudentHomeworkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Student: api"])
    def get(self, request):
        objects = HomeWork.objects.filter(group_id=request.user.group_id)
        if objects.exists():
            serializer = HomeworkSerializer(instance=objects, many=True)
            return JsonResponse({"message": "Homeworks were found", "status": "200", "data": serializer.data})
        return JsonResponse({"message": "Homeworks not found", "status": "404"})


class StudentHomeworkSubmitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=SubmissionSerializer, tags=["Student: api"])
    def post(self, request, pk):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.data['homework_id'] = pk
            serializer.save()
            return JsonResponse({"message": "Submission created successfully.", "status": "200", "data": serializer.data})
        return JsonResponse({"message": "There was an error creating the submission.", "status": "500"})
