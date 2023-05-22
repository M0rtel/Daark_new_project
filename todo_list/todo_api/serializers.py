import logging

from rest_framework import serializers

from .models import List, Task, Folder


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class ListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    logging.info(tasks)

    class Meta:
        model = List
        fields = "__all__"


class FolderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    logging.info(user)
    lists = ListSerializer(many=True, read_only=True)
    logging.info(lists)

    class Meta:
        model = Folder
        fields = "__all__"


# class FolderSerializer(serializers.Serializer):
#     user = serializers.CharField()
#     title = serializers.CharField(max_length=75)
#     created = serializers.DateTimeField(read_only=True)
#     updated = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         return Folder.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.created = validated_data.get('created', instance.created)
#         instance.updated = validated_data.get('updated', instance.updated)
#         return instance
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response(
#                 {'error': 'Method PUT not allowed'}
#             )
#
#         try:
#             instance = Folder.objects.get(pk=pk)
#
#         except:
#             return Response(
#                 {'error': 'Object doex not exists'}
#             )
#
#         serializer = FolderSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {'post_put': serializer.data}
#         )
#
#
