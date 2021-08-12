from django.urls import path
from . import views


urlpatterns = [
    path('tims/', views.ListTimAPIView.as_view(), name='tims'),
    path('tim/<int:id>/like/', views.LikeTimAPIView.as_view(), name='tim_like'),
    path('tim/<int:id>/co-host/', views.JoinTimAPIView.as_view(), name='co_host'),
    path('tim/<int:id>/', views.DetailTimAPIView.as_view(), name='tim'),
    path('tim/create/', views.CreateTimAPIView.as_view(), name='create'),
    path('tim/delete/<int:id>/', views.DeleteTimAPIView.as_view(), name='delete'),
    path('comments/', views.CommentAPIView.as_view(), name='comments'),
    path('comment/<int:id>/like/', views.LikeCommentAPIView.as_view(), name='comment_like'),
    path('comment/<int:pk>/', views.CommentAPIView.as_view(), name='delete-comment'),
]