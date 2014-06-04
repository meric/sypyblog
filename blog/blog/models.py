from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate


class Post(models.Model):
    content = models.TextField(max_length=256)
    author = models.ForeignKey('auth.User')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return (" by ").join([self.content, self.author.username])


class Comment(models.Model):
    post = models.ForeignKey('Post')
    content = models.TextField(max_length=256)
    author = models.ForeignKey('auth.User')
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return (" by ").join([self.content, self.author.username])


def create_users(*args, **kwargs):
    if not User.objects.filter(username="eric").exists():
        user = User.objects.create_user(
            username="eric",
            password="eric")
        user.is_staff=True
        user.save()

post_migrate.connect(create_users)
