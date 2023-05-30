from .models import List, Task, Folder

from rest_framework import serializers

from .models import User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'token',)

        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """

        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    modify_by = serializers.PrimaryKeyRelatedField(read_only=True)
    # old_version = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class ListSerializer(serializers.ModelSerializer):
    # tasks = TaskSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    modify_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = List
        fields = "__all__"


class FolderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Folder
        fields = "__all__"
