from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('check-user/', check_user_is_authenticated, name='check-user'),
    path('logout/', logout_user, name='logout'),
]