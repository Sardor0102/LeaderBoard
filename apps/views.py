from http import HTTPStatus

from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from apps.serializers import RegisterModelSerializer


# Create your views here.


@extend_schema(tags=['auth'])
class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer
    permission_classes = (AllowAny,)



@extend_schema(tags=['auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['auth'])
class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'status': HTTPStatus.OK, 'message': 'Logout successful!'})
        except Exception as e:
            return Response({'status': HTTPStatus.BAD_REQUEST, 'message': 'Logout failed!'})


