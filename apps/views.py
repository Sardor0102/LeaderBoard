from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.serializers import *

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
