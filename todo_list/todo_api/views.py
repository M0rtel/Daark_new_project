import logging

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Folder, List, Task
from .permissions import AuthenticatedPOST
from .serializers import FolderSerializer, ListSerializer


class V1APIView(APIView):
    def get(self, request):
        return Response(
            {
                'folders': 'http://127.0.0.1:8000/api/v1/folders/',
                'lists': 'http://127.0.0.1:8000/api/v1/lists/',
                'tasks': 'http://127.0.0.1:8000/api/v1/tasks/',
                'auth': [
                    'http://127.0.0.1:8000/api/v1/auth/',
                    'http://127.0.0.1:8000/api/v1/auth/token/',
                    'http://127.0.0.1:8000/api/v1/auth/token/refresh/',
                    'http://127.0.0.1:8000/api/v1/auth/token/verify/',
                ]
            }
        )


# FOLDER
class FolderAPIViewGetPost(APIView):
    serializer_class = FolderSerializer
    permission_classes = [AuthenticatedPOST]

    # get
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user_get_folder = self.check_privilege()
        logging.info(user_get_folder)
        serializer = FolderSerializer(user_get_folder, many=True)
        logging.info(serializer.data)
        return Response(serializer.data)

    def check_privilege(self):
        user = self.request.user
        objs = Folder.objects.all()

        user_get_folder = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (obj.user == user) and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (user in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_folder):
                user_get_folder.append(obj)

        return user_get_folder

    # post
    def post(self, request):
        if request.user.is_authenticated:
            serializer = FolderSerializer(data=request.data)

            logging.info(serializer)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                logging.info(serializer.data)
                logging.info(type(serializer.data))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logging.info(serializer.errors)
            logging.info(type(serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "У вас недостаточно прав."})


class FolderAPIViewUpdateDeleteGet(APIView):  # odj == 'ТО ЧТО уже есть в БД'  request == 'ТО что сейчас ты твоё состояние'
    serializer_class = FolderSerializer
    permission_classes = [AuthenticatedPOST]

    def get_object(self, pk):
        try:
            return Folder.objects.get(pk=pk)
        except Folder.DoesNotExist:
            raise Http404

    # get
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = Folder.objects.get(pk=kwargs['pk'])
        serializer = FolderSerializer(instance=instance)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        objs = Folder.objects.all()

        user_get_folder = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (obj.user == user) and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (user in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_folder):
                user_get_folder.append(obj)

        serializer = FolderSerializer(user_get_folder, many=True)
        return Response(serializer.data)

    # delete
    def delete(self, request, pk):
        obj = self.get_object(pk)
        logging.info(obj.user)
        logging.info(request.user)
        if obj.user == request.user:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "У вас недостаточно прав."})

    # put
    def put(self, request, pk):
        obj = self.get_object(pk)
        if obj.user == request.user:
            serializer = FolderSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "У вас недостаточно прав."})


# LIST
class ListAPIViewGetPost(APIView):
    serializer_class = ListSerializer
    permission_classes = [AuthenticatedPOST]

    # get
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user_get_folder = self.check_privilege()
        logging.info(user_get_folder)
        serializer = ListSerializer(user_get_folder, many=True)
        logging.info(serializer.data)
        return Response(serializer.data)

    def check_privilege(self):
        user = self.request.user
        objs = List.objects.all()

        user_get_folder = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (obj.user == user) and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (user in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_folder):
                user_get_folder.append(obj)

        return user_get_folder

    # post
    def post(self, request):
        if request.user.is_authenticated:
            serializer = ListSerializer(data=request.data)
            logging.info(serializer)
            if serializer.is_valid():
                serializer.save(
                    user=self.request.user,
                )
                data_s = serializer.data
                logging.info(data_s)
                list_parent_folder = self.check_parent_folder()
                logging.info(list_parent_folder)
                logging.info(data_s['parent_folder'])
                if data_s['parent_folder'] in list_parent_folder:
                    return Response(data_s, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "У вас недостаточно прав."})

            logging.info(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "У вас недостаточно прав."})

    def check_parent_folder(self):
        user = self.request.user
        objs = Folder.objects.all()

        parent_folder_l = []
        for obj in objs:
            if obj.is_public and (obj not in parent_folder_l):
                parent_folder_l.append(obj)

            elif (obj.user == user) and (obj not in parent_folder_l):
                parent_folder_l.append(obj)

            elif (user in [user.username for user in obj.authorized_users.all()]) and (obj not in parent_folder_l):
                parent_folder_l.append(obj)

        parent_folder_list = [x.id for x in parent_folder_l]
        return parent_folder_list


class ListAPIViewUpdateDeleteGet(APIView):  # odj == 'ТО ЧТО уже есть в БД' request == 'ТО что сейчас ты твоё состояние'
    serializer_class = ListSerializer
    permission_classes = [AuthenticatedPOST]

    def get_object(self, pk):
        try:
            return List.objects.get(pk=pk)
        except List.DoesNotExist:
            raise Http404

    # get
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = List.objects.get(pk=kwargs['pk'])
        serializer = ListSerializer(instance=instance)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        objs = List.objects.all()

        user_get_folder = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (obj.user == user) and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (user in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_folder):
                user_get_folder.append(obj)

        serializer = ListSerializer(user_get_folder, many=True)
        return Response(serializer.data)

    # delete
    def delete(self, request, pk):
        obj = self.get_object(pk)
        logging.info(obj.user)
        logging.info(request.user)
        if obj.user == request.user:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "У вас недостаточно прав."})

    # put
    def put(self, request, pk):
        obj = self.get_object(pk)
        if obj.user == request.user:
            serializer = ListSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "У вас недостаточно прав."})


# def get_queryset(self):
#     user = self.request.user
#     # logging.info(user)
#     # logging.info(Folder.objects.all()[0].user)
#     # logging.info(Folder.objects.all()[0].authorized_user_read)
#     user_get_folder = []
#     for obj in Folder.objects.all():
#         if obj.user == user or obj.authorized_user_read:
#             user_get_folder.append(obj)
#
#     return user_get_folder

# class FolderAPIList(generics.ListAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer
#     permission_classes = [AuthenticatedPOST]
#
#     def get_queryset(self):
#         user = self.request.user
#         # logging.info(user)
#         # logging.info(Folder.objects.all()[0].user)
#         # logging.info(Folder.objects.all()[0].authorized_user_read)
#         user_get_folder = []
#         for obj in Folder.objects.all():
#             if obj.user == user or obj.authorized_user_read:
#                 user_get_folder.append(obj)
#
#         return user_get_folder
#
#
# class FolderAPICreate(generics.CreateAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer
#     permission_classes = [AuthorOrReadOnly]


# class FolderAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer
#     permission_classes = [AuthorOrReadOnly]


# class FolderViewSet(viewsets.ModelViewSet):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer
#     permission_classes = [AuthorOrReadOnly]
#     """
#         The GenericViewSet class does not provide any actions by default,
#         but does include the base set of generic view behavior, such as
#         the `get_object` and `get_queryset` methods.
#     """
#     # def check_permissions(self, request):
#     #     for permission in self.get_permissions():
#     #         if not permission.has_permission(request, self):
#     #             self.permission_denied(
#     #                 request,
#     #                 message=getattr(permission, 'message', None),
#     #                 code=getattr(permission, 'code', None)
#     #             )
#     #
#     # def check_object_permissions(self, request, obj):
#     #     for permission in self.get_permissions():
#     #         if not permission.has_object_permission(request, self, obj):
#     #             self.permission_denied(
#     #                 request,
#     #                 message=getattr(permission, 'message', None),
#     #                 code=getattr(permission, 'code', None)
#     #             )
#     # def get_object(self):
#     #     unauthorized_user_read = self.obj.unauthorized_user_read
#     #     logging.info(unauthorized_user_read)
#
#     def get_queryset(self):
#         user = self.request.user
#         logging.info(user)
#         logging.info(Folder.objects.all()[0].user)
#         logging.info(Folder.objects.all()[0].authorized_user_read)
#         user_get_folder = []
#         for obj in Folder.objects.all():
#             if obj.user == user or obj.authorized_user_read:
#                 user_get_folder.append(obj)
#
#         return user_get_folder


# class ListViewSet(viewsets.ModelViewSet):
#     queryset = List.objects.all()
#     serializer_class = ListSerializer
#     permission_classes = [AuthorOrReadOnly]

    # def get_queryset(self):
    #     user = self.request.user
    #     return List.objects.filter(parent_folder__user=user)


# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [AuthorOrReadOnly]

    # def get_queryset(self):
    #     return Task.objects.all()





# class FolderAPIList(generics.ListAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer
#     permission_classes = [AuthorOrReadOnly]
#
#
# class FolderAPICreate(generics.CreateAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer
#     permission_classes = [AuthorOrReadOnly]
#
#
# class FolderAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer
#     permission_classes = [AuthorOrReadOnly]
#
#
# class ListAPIList(generics.ListAPIView):
#     queryset = List.objects.all()
#     serializer_class = ListSerializer
#     permission_classes = [AuthorOrReadOnly]
#
#
# class ListAPICreate(generics.CreateAPIView):
#     queryset = List.objects.all()
#     serializer_class = ListSerializer
#     permission_classes = [AuthorOrReadOnly]
#
#
# class ListAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = List.objects.all()
#     serializer_class = ListSerializer
#     permission_classes = [AuthorOrReadOnly]
#
#
# class TaskAPIList(generics.ListAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [AuthorOrReadOnly]
#
#
# class TaskAPICreate(generics.CreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [AuthorOrReadOnly]
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
# class TaskAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [AuthorOrReadOnly]
