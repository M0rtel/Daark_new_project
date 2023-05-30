import jwt

from datetime import datetime, timedelta

from django.conf import settings


from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


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
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modify_list')  # Пользователь который последний раз вносил изменения
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
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modify_task')  # Пользователь который последний раз вносил изменения
    parent_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=75)
    is_public = models.BooleanField(default=False, blank=True)
    authorized_users = models.ManyToManyField(User, blank=True)  # сделать связь многих ко многим(CRUD)
    statues = models.TextChoices('StatusTask', 'DONE PROCESS CANCEL')
    status = models.CharField(choices=statues.choices, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # old_version = models.ForeignKey('self', on_delete=models.CASCADE) ???

    def __str__(self):
        return self.title
