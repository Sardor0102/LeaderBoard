from django.db import models
from django.contrib.auth.models import AbstractUser


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

    class Meta:
        db_table = 'courses'



