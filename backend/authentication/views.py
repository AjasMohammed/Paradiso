from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LogInSerializer
from django.contrib.auth import logout, authenticate, login
from rest_framework.decorators import api_view

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator 




class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            print('Saved')
            serializer.save()
            
            return Response({'message': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        print('Not Saved')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({'message': 'LoggedIn Successufully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "User Dosen't Exists"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def check_user_is_authenticated(request):
    authenticated = request.user.is_authenticated

    return Response(authenticated, status=status.HTTP_200_OK)


def logout_user(request):
    logout(request)
    return Response({'message': 'User Logged Out Successfully'}, status=status.HTTP_200_OK)








@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCsrfToken(APIView):

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})