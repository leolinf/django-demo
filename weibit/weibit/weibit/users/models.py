from django.db import models
from django.contrib.auth.models import User


class UserAdd(User):

    phone = models.CharField(max_length=11)


class Snippet(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(max_length=100)
    style = models.CharField(max_length=100)

    class Meta:
        ordering = ('created',)
