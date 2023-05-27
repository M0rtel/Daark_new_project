from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    # user = models.CharField(User.username, default=User.username)
    title = models.CharField(max_length=75)
    is_public = models.BooleanField(default=False, blank=True)
    authorized_users = models.ManyToManyField(User, blank=True)  # сделать связь многих ко многим(read)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_list')
    modify_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modify_list')  # Пользователь который последний раз вносил изменения
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='lists')
    title = models.CharField(max_length=75)
    is_public = models.BooleanField(default=False, blank=True)
    authorized_users = models.ManyToManyField(User, blank=True)  # сделать связь многих ко многим(CRUD)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_task')
    modify_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modify_task')  # Пользователь который последний раз вносил изменения
    parent_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=75)
    authorized_users = models.ManyToManyField(User, blank=True)  # сделать связь многих ко многим(CRUD)
    statues = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
    status = models.CharField(blank=True, choices=statues.choices, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    old_version = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
