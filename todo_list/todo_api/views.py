import logging

from rest_framework import viewsets, generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Folder, List, Task
from .permissions import IsAdminOrReadOnly
from .serializers import FolderSerializer, ListSerializer, TaskSerializer


class V1APIView(APIView):
    def get(self, request):
        return Response(
            {
                'folders': 'http://127.0.0.1:8000/api/v1/folders',
                'lists': 'http://127.0.0.1:8000/api/v1/lists',
                'tasks': 'http://127.0.0.1:8000/api/v1/tasks',
            }
        )


class FolderAPIList(generics.ListAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FolderAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class ListAPIList(generics.ListAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class ListAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class TaskAPIList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# class FolderViewSet(viewsets.ModelViewSet):
#     queryset = Folder.objects.all()
#     logging.info(queryset)
#     serializer_class = FolderSerializer
#     # permission_classes = [IsAdminOrReadOnly]
#
#     def get_queryset(self):
#         user = self.request.user
#         logging.info(Folder.objects.filter(user=user))
#         return Folder.objects.filter(user=user)
#
#
# class ListViewSet(viewsets.ModelViewSet):
#     queryset = List.objects.all()
#     logging.info(queryset)
#     serializer_class = ListSerializer
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get_queryset(self):
#         user = self.request.user
#         logging.info(List.objects.filter(parent_folder__user=user))
#         return List.objects.filter(parent_folder__user=user)
#
#
# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     logging.info(queryset)
#     serializer_class = TaskSerializer
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get_queryset(self):
#         logging.info(Task.objects.all())
#         return Task.objects.all()



# class FolderAPIView(APIView):
#     def get(self, request):
#         w = Folder.objects.all()
#         return Response(
#             {'folders_get': FolderSerializer(w, many=True).data}
#         )
#
#     def post(self, request):
#         serializer = FolderSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(
#             {'folders_post': serializer.data}
#         )
