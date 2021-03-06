from django.db import models
from users.models import CustomUser
from django.utils.text import slugify
# Create your models here.


class Tim(models.Model):
    host = models.ForeignKey(CustomUser, related_name='host', on_delete=models.CASCADE)
    co_host = models.ManyToManyField(CustomUser, related_name='co_host', blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    likes = models.ManyToManyField(to=CustomUser, related_name='tim_likes', blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='uploads/tim/images', blank=False, null=False)
    location = models.CharField(max_length=250, blank=False, null=False)
    tim_date_time = models.DateTimeField()
    participants = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, related_name='comment_user', on_delete=models.CASCADE)
    tim = models.ForeignKey(Tim, related_name='tim', on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    likes = models.ManyToManyField(to=CustomUser, related_name='comment_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.tim.title
