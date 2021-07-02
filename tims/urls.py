from django.urls import path
from . import views


urlpatterns = [
    path('tim/', views.ListTimAPIView.as_view(), name='tim'),
    path('tim/<int:id>/', views.DetailTimAPIView.as_view(), name='details'),
    path('tim/create/', views.CreateTimAPIView.as_view(), name='create'),
    path('tim/delete/<int:id>/', views.DeleteTimAPIView.as_view(), name='delete'),
    path('comments/', views.CommentAPIView.as_view(), name='comment'),
    path('comments/<int:pk>/', views.CommentAPIView.as_view(), name='delete-comment'),
    path('like/', views.LikeAPIView.as_view(), name='like'),
    # path('like/<int:pk>/', views.LikeAPIView.as_view(), name='like-update'),

]