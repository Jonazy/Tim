from .models import Tim, Comment
from users.models import CustomUser
from rest_framework import serializers
from datetime import datetime


class TimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tim
        fields = ['id', 'host', 'co_host', 'title', 'description', 'likes', 'slug', 'image', 'location', 'tim_date_time',
                  'participants', 'created_at', 'updated_at']
        # read_only_fields = ['host']

    def validate(self, attrs):
        co_host = attrs.get('co_host')
        co_host = list(co_host)
        tim_date_time = attrs.get('tim_date_time')
        participants = attrs.get('participants')

        # if len(co_host_set) > 5:
        #     raise serializers.ValidationError("You can only add 5 host to your Tim")
        if tim_date_time.date() < datetime.now().date():
            raise serializers.ValidationError("Date must be in future")
        if tim_date_time.date() == datetime.now().date() and tim_date_time.time() < datetime.now().time():
            raise serializers.ValidationError("Time must be in future")
        if participants < 1 > 25:
            raise serializers.ValidationError("Participant must be greater than 0 and max 25")
        return super().validate(attrs)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    tim = serializers.PrimaryKeyRelatedField(queryset=Tim.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tim', 'comment', 'likes', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    # tim = serializers.PrimaryKeyRelatedField(queryset=Tim.objects.all())

    class Meta:
        model = Tim
        fields = ['id', 'host', 'tim', 'like']

    def validate(self, attrs):
        tim = attrs.get('tim')
        tim_obj = Tim.objects.get(id=tim)
        host = attrs.get('host')
        get_user = CustomUser.objects.get(id=host)
        like = attrs.get('like')

        if not tim_obj.like:
            like = True
        else:
            like = False
        return attrs


# class LikeSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
#     tim = serializers.PrimaryKeyRelatedField(queryset=Tim.objects.all())
#
#     class Meta:
#         model = Like
#         fields = ['id', 'user', 'tim', 'like', 'created_at', 'updated_at']
#
#     def validate(self, attrs):
#         user = attrs.get('user')
#         like = attrs.get('like')
#         tim = attrs.get('tim')
#         like_by_user = Like.objects.filter(user=user)
#         like_by_tim = Tim.objects.filter(id=tim.id)
#         print(like_by_tim)
#         likes = Like.objects.all()
#         print(likes.filter_by)
#         if like_by_tim == "First time":
#             raise serializers.ValidationError('You have already liked this Tim')
#         else:
#             like = True
#         return attrs

