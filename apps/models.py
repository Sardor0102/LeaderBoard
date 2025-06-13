from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import CharField, TextField, DateTimeField


# Create your models here.


class Course(Model):
    name = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Group(Model):
    name = CharField(max_length=255)
    course_id = ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.course_id.name}"


class Badge(models.Model):
    name = CharField(max_length=255)
    icon = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name








