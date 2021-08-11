from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TimSerializer, CommentSerializer, LikeSerializer
from .models import Tim, Comment
from .permissions import IsHost


# Create your views here.


class ListTimAPIView(generics.ListAPIView):
    queryset = Tim.objects.all()
    serializer_class = TimSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)


class CreateTimAPIView(generics.CreateAPIView):
    queryset = Tim.objects.all()
    serializer_class = TimSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()


class DetailTimAPIView(generics.RetrieveAPIView):
    queryset = Tim.objects.all()
    serializer_class = TimSerializer
    lookup_field = "id"
    # permission_classes = (permissions.IsAuthenticated,)


class DeleteTimAPIView(generics.DestroyAPIView):
    queryset = Tim.objects.all()
    serializer_class = TimSerializer
    lookup_field = "id"
    permission_classes = (permissions.IsAuthenticated, IsHost,)


class CommentAPIView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)

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


class LikeAPIView(APIView):
    def get(self, request):
        queryset = Tim.objects.all()
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = LikeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = request.user
        serializer = LikeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class LikeAPIView(APIView):
#     # permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request):
#         queryset = Like.objects.all()
#         serializer = LikeSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = LikeSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user)
#             return Response({'message': 'like successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # if serializer.is_valid(raise_exception=True):
#         #     if request.user not in queryset:
#         #         serializer.data['like_or_dislike'] = True
#         #         serializer.save(user=request.user)
#         #         return Response({'message': 'like successfully'}, status=status.HTTP_201_CREATED)
#         #
#         #     elif request.user in tim.user.like_or_dislike == True:
#         #         serializer.save(request.user)
#         #         return Response({'message': 'Dislike successfully'}, status=status.HTTP_201_CREATED)
#         #
#         #     else:
#
