from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.UserListAPIView.as_view()),
    path('user/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-details'),
    path('user/<int:pk>/update/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', views.UserDeleteAPIView.as_view(), name='user-update'),
    path('registration/', views.UserRegistrationAPIView.as_view(), name='register-user'),
    path('verify-email/', views.VerifyEmailAPIView.as_view(), name='verify-email'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('password-reset-email/', views.RequestPasswordResetAPIView.as_view(), name='password-reset-email'),
    path('password-reset-token-check/<uidb64>/<token>/', views.PasswordResetTokenCheck.as_view(),
         name='password-reset-token-check'),
    path('password-reset/', views.SetNewPasswordAPIView.as_view(),
         name='password-reset'),

]

urlpatterns = format_suffix_patterns(urlpatterns)