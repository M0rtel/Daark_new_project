import logging

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Folder, List, Task
from .serializers import FolderSerializer, ListSerializer, TaskSerializer


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logging.info(user)
        logging.info(Folder.objects.filter(user=user))
        return Folder.objects.filter(user=user)


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logging.info(List.objects.filter(parent_folder__user=user))
        return List.objects.filter(parent_folder__user=user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logging.info(Task.objects.all())
        return Task.objects.all()


# class FolderAPIList(generics.ListCreateAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer
#
# class FolderAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer

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
