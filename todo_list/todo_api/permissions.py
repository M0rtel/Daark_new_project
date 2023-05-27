import logging

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):  # настройка прав доступа на уровне всего запроса клиента
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):  # настройка прав доступа на уровне определённого объекта
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


# Этот класс разрешений разрешает доступ к нему только автору объекта:
# В has_permission мы отказываем в разрешении только неаутентифицированным пользователям.
# На данный момент у нас нет доступа к объекту, поэтому мы не знаем, является ли пользователь, делающий запрос, автором желаемого объекта.
# Если пользователь аутентифицирован, после получения объекта вызывается has_object_permission, где мы проверяем,
# совпадает ли автор объекта с пользователем.
class AuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class AuthenticatedPOST(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
