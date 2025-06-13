from django.db import models
from django.contrib.auth.models import AbstractUser


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

    class Meta:
        db_table = 'courses'


class User(AbstractUser):
    ROLE_CHOICES = [('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')]
    LEVEL_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return f"{self.fullname} - {self.role}"

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Assignment(models.Model):
    ASSIGNMENT_TYPE_CHOICES = [('homework', 'Homework'), ('project', 'Project'), ('exam', 'Exam'), ('quiz', 'Quiz'),
                               ('lab', 'Lab Work')]
    DIFFICULTY_CHOICES = [(1, 'Very Easy'), (2, 'Easy'), (3, 'Medium'), (4, 'Hard'), (5, 'Very Hard')]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=3)
    deadline = models.DateTimeField(blank=True, null=True)
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPE_CHOICES, default='homework')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return f"Assignment #{self.id} - {self.title} - {self.assignment_type}"

    class Meta:
        db_table = 'assignments'
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        ordering = ['-created_at']


class UserAssignment(models.Model):
    STATUS_CHOICES = [('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('submitted', 'Submitted'),
                      ('graded', 'Graded'), ('completed', 'Completed')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_assignments')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='user_assignments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    submitted_at = models.DateTimeField(blank=True, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return f"{self.user.fullname} - {self.assignment.title} - {self.status}"

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








