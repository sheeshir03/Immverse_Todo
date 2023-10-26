from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate
from todo_test_db.models import Users


# Create your views here.


class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),

            },
                status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'User Name or Password is Wrong! Please Try Again with Correct Credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        

class Register(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        date_of_birth = request.data.get('date_of_birth')

        if not username or not password or not email:
            return Response({'error': 'Please provide username, password, and email'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = Users.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        refresh = RefreshToken.for_user(user)

        return Response({'access_token': str(refresh.access_token),
                         'refresh_token': str(refresh)},
                        status=status.HTTP_201_CREATED)
