from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    title = models.CharField(max_length=75)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class List(models.Model):
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='lists')
    title = models.CharField(max_length=75)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    parent_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=75)
    completed = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
