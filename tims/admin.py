from django.contrib import admin
from .models import Comment, Tim

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tim', 'comment',)


admin.site.register(Comment, CommentAdmin)


class TimAdmin(admin.ModelAdmin):
    list_display = ('id', 'host', 'title', 'description', 'slug', 'image', 'location',
                    'tim_date_time', 'participants', 'created_at', 'updated_at',)


admin.site.register(Tim, TimAdmin)
