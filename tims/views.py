from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TimSerializer, CommentSerializer
from .models import Tim, Comment
from .permissions import IsHost
from django.http import HttpResponse

# Create your views here.


class ListTimAPIView(generics.ListAPIView):
    queryset = Tim.objects.all()
    serializer_class = TimSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)


class CreateTimAPIView(generics.CreateAPIView):
    queryset = Tim.objects.all()
    serializer_class = TimSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()


class DetailTimAPIView(generics.RetrieveAPIView):
    queryset = Tim.objects.all()
    serializer_class = TimSerializer
    lookup_field = "id"
    permission_classes = (permissions.IsAuthenticated,)


class DeleteTimAPIView(generics.DestroyAPIView):
    queryset = Tim.objects.all()
    serializer_class = TimSerializer
    lookup_field = "id"
    permission_classes = (permissions.IsAuthenticated, IsHost,)


class LikeTimAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        queryset = Tim.objects.all()
        tim = get_object_or_404(queryset, id=id)
        user = request.user
        if user in tim.likes.all():
            tim.likes.remove(user)
            return Response({"success": "unliked"}, status=status.HTTP_201_CREATED)
        else:
            tim.likes.add(user)
            return Response({"success": "Liked"}, status=status.HTTP_201_CREATED)


class CommentAPIView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        permission_classes = (permissions.IsAuthenticated, IsHost)
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, id=id)
        serializer = CommentSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        permission_classes = (permissions.IsAuthenticated, IsHost)
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        comment.delete()
        return Response({'message': 'comment deleted successfully'}, status=status.HTTP_404_NOT_FOUND)


class LikeCommentAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, id):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, id=id)
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            return Response({"success": "unliked"}, status=status.HTTP_201_CREATED)
        else:
            comment.likes.add(user)
            return Response({"success": "Liked"}, status=status.HTTP_201_CREATED)


class JoinTimAPIView(APIView):
    """endpoint for a login user to join a tim if he is not a host, yet to join and is login"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        queryset = Tim.objects.all()
        tim = get_object_or_404(queryset, id=id)
        user = request.user
        if tim.co_host.all().count() >= tim.participants:
            return Response({"error": "number of participant is full"}, status=status.HTTP_200_OK)
        elif user == tim.host:
            return Response({"error": "you can't join own tim"}, status=status.HTTP_200_OK)
        elif user in tim.co_host.all():
            return Response({"error": "already joined tim"}, status=status.HTTP_200_OK)
        else:
            tim.co_host.add(user)
            return Response({"success": "Joined"}, status=status.HTTP_201_CREATED)
