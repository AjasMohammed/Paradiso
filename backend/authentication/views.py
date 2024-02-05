import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LogInSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


class RegisterUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'Registration Successful'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        context = {}
        if serializer.is_valid():
            context['data'] = serializer.validated_data
            data = serializer.validated_data
            context['access_token'] = data['access']
            response = Response(context, status=status.HTTP_200_OK)
            response.set_cookie(
                key='refresh_token',
                value=data['refresh'],
                httponly=True,
                secure=False,
                expires=datetime.datetime.now() + datetime.timedelta(days=90)
            )
            return response
        context['message'] = serializer.errors
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class LogOutUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"message": "refresh token is missing!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(
                {'message': "Successfully LoggedOut!"}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token')
            return response
        except:
            return Response({"message": "token is invalid!"}, status=status.HTTP_404_NOT_FOUND)


class CheckAuthenticationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCsrfToken(APIView):

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})
