from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
    path('user/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)