import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer


class RegisterModelSerializer(ModelSerializer):
    phone = CharField(max_length=20)
    class Meta:
        model = User
        fields = 'id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone'

    def validate_password(self, value):
        return make_password(value)

    def validate_phone(self, value):
        return re.sub('\D', '', value)




