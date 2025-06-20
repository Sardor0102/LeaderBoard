from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models import *


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLE = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin')
    ]

    email = EmailField(unique=True)
    first_name = CharField(max_length=150, null=True, blank=True)
    last_name = CharField(max_length=150, null=True, blank=True)
    phone_number = CharField(max_length=25, blank=True, null=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    role = CharField(max_length=20, choices=USER_ROLE)
    group = ForeignKey('apps.Group', on_delete=SET_NULL, null=True, related_name="students")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_fullname()


class Curse(Model):
    title = CharField(max_length=100)
    code = CharField(max_length=2)

    def __str__(self):
        return self.title


class Group(Model):
    name = CharField(max_length=10, unique=True)
    teacher = ForeignKey('apps.User', on_delete=SET_NULL, null=True, related_name="teacher_groups")
    curse = ForeignKey('apps.Curse', on_delete=SET_NULL, null=True, related_name="curse_groups")

    def save(self, *args, **kwargs):
        count = Group.objects.filter(curse__code=self.curse.code).count() + 1
        self.name = f"{self.curse.code}{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class HomeWork(Model):
    title = CharField(max_length=255)
    description = TextField()
    points = PositiveIntegerField()
    start_date = DateTimeField(null=True)
    deadline = DateTimeField(null=True)
    line_limit = PositiveIntegerField()
    teacher = ForeignKey('apps.User', on_delete=SET_NULL, null=True, related_name="homeworks")
    group = ForeignKey('apps.Group', on_delete=SET_NULL, null=True, related_name="homeworks")
    file_extension = CharField(max_length=100)
    ai_grading_prompt = TextField()
    created_at = DateTimeField(auto_now_add=True)


class Submission(Model):
    homework = ForeignKey('apps.HomeWork', on_delete=SET_NULL, null=True, related_name="submissions")
    student = ForeignKey('apps.User', on_delete=SET_NULL, null=True, related_name="submissions")
    ai_grade = PositiveIntegerField()
    final_grade = PositiveIntegerField()
    ai_feedback = CharField(max_length=255)
    submitted_at = DateTimeField(auto_now_add=True)


class SubmissionFile(Model):
    name = CharField(max_length=255)
    submission = ForeignKey('apps.Submission', on_delete=SET_NULL, null=True, related_name="files")
    content = TextField()
    line_count = PositiveIntegerField()


class Grade(Model):
    submission = ForeignKey('apps.Submission', on_delete=SET_NULL, null=True, related_name="grades")
    ai_task_completeness = PositiveIntegerField()
    ai_code_quality = PositiveIntegerField()
    ai_correctness = PositiveIntegerField()
    ai_total = PositiveIntegerField()

    final_task_completeness = PositiveIntegerField()
    final_code_quality = PositiveIntegerField()
    final_correctness = PositiveIntegerField()
    final_total = PositiveIntegerField()

    ai_feedback = CharField(max_length=255)
    task_completeness_feedback = CharField(max_length=255)
    code_quality_feedback = CharField(max_length=255)
    correctness_feedback = CharField(max_length=255)
    modified_by_teacher = CharField(max_length=255)



