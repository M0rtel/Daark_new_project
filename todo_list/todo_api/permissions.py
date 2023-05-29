import logging
from rest_framework import permissions


# Этот класс разрешений разрешает доступ к нему только автору объекта:
# В has_permission мы отказываем в разрешении только неаутентифицированным пользователям.
# На данный момент у нас нет доступа к объекту, поэтому мы не знаем, является ли пользователь,
# делающий запрос, автором желаемого объекта.
# Если пользователь аутентифицирован, после получения объекта вызывается has_object_permission, где мы проверяем,
# совпадает ли автор объекта с пользователем.
# class AuthorOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if obj.user == request.user:
#             return True
#         return False


class Authenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
