from django.db import models
from django.contrib.auth.models import User


class SimpleUser(models.Model):
    """Model for simple user on platform."""
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class UserPost(models.Model):
    """Model with post information"""
    title = models.CharField(max_length=150, verbose_name='Name')
    content = models.TextField(blank=True, verbose_name='Describe')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    update = models.DateTimeField(auto_now=True, verbose_name='Update')
    image = models.ImageField(upload_to='photo/%Y/%m/%d', verbose_name='Image')
    is_published = models.BooleanField(default=True, verbose_name='Publish')
    author = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, verbose_name='Author')

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    content = models.TextField(verbose_name='Content')

    def __str__(self):
        return self.user.username
