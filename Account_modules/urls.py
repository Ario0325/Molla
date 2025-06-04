# from django.urls import path
#
# from Account_modules.views import *
#
# urlpatterns = [
#     path('Login-register/', Login.as_view(), name="Login-Register"),
#     path('logout/',LogoutUserView.as_view(),name = 'logout'),
#     path('register/',RegisterView.as_view(),name = 'register')
# ]
#
from django.urls import path
from .views import Login, RegisterView, logout_view, ProfileView, PasswordResetView

urlpatterns = [
    path('login-register/', Login.as_view(), name="Login-Register"),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
]
