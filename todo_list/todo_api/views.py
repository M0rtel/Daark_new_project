import logging

from django.http import Http404
from rest_framework.pagination import PageNumberPagination

from .models import Folder, List, Task
from .permissions import Authenticated
from .serializers import FolderSerializer, ListSerializer, TaskSerializer

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)

log = logging.getLogger('nav_info')


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        log.info(
            f"Registration - "
            f"IP: {request.META['REMOTE_ADDR']}, User-Agent:"
            f" {request.META['HTTP_USER_AGENT']}, ID: {serializer.data['id']}"
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        log.info(
            f"Login - "
            f"IP: {request.META['REMOTE_ADDR']}, User-Agent:"
            f" {request.META['HTTP_USER_AGENT']}"
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        log.info(
            f"UserRetrieveUpdate - "
            f"IP: {request.META['REMOTE_ADDR']}, User-Agent:"
            f" {request.META['HTTP_USER_AGENT']}, ID: {serializer.data['id']}"
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        log.info(
            f"UserRetrieveUpdate - "
            f"IP: {request.META['REMOTE_ADDR']}, User-Agent:"
            f" {request.META['HTTP_USER_AGENT']}, ID: {serializer.data['id']}"
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


# class LargeResultsSetPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 10000


class V1APIView(APIView):
    def get(self, request):
        return Response(
            {
                'folders': 'http://127.0.0.1:8000/api/v1/folders/',
                'lists': 'http://127.0.0.1:8000/api/v1/lists/',
                'tasks': 'http://127.0.0.1:8000/api/v1/tasks/',
                'auth': [
                    'http://127.0.0.1:8000/api/v1/user',
                    'http://127.0.0.1:8000/api/v1/users/',
                    'http://127.0.0.1:8000/api/v1/users/login/'
                ]
            }
        )


# --------------------------Folder----------------------------


class FolderAPIViewGetPost(APIView):
    serializer_class = FolderSerializer
    permission_classes = [Authenticated]
    # pagination_class = LargeResultsSetPagination

    # get
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user_get_folder = self.check_privilege()
        serializer = FolderSerializer(user_get_folder, many=True)
        log.info(f'READ: {serializer.data}')
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

            elif (str(user) in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_folder):
                user_get_folder.append(obj)

        return user_get_folder

    def post(self, request):
        if request.user.is_authenticated:
            serializer = FolderSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=self.request.user)
                log.info(f'CREATED, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "У вас недостаточно прав."})


class FolderAPIViewUpdateDeleteGet(APIView):
    serializer_class = FolderSerializer
    permission_classes = [Authenticated]

    def get_object(self, pk):
        try:
            return Folder.objects.get(pk=pk)
        except Folder.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = Folder.objects.get(pk=kwargs['pk'])
            serializer = FolderSerializer(instance=instance)
            log.info(f'READ, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
            return Response(serializer.data)
        except Folder.DoesNotExist:
            raise Http404

    def get_queryset(self):
        user = self.request.user
        objs = Folder.objects.all()

        user_get_folder = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (obj.user == user) and (obj not in user_get_folder):
                user_get_folder.append(obj)

            elif (str(user) in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_folder):
                user_get_folder.append(obj)

        serializer = FolderSerializer(user_get_folder, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if obj.user == request.user:
            obj.delete()
            log.info(f'DELETED - "delete_folder_id": {pk}')
            return Response({"delete_folder_id": pk}, status=status.HTTP_200_OK)

        return Response({"detail": "У вас недостаточно прав."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if obj.user == request.user:
            serializer = FolderSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                log.info(f'UPDATED, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "У вас недостаточно прав."})


# --------------------------List----------------------------


class ListAPIViewGetPost(APIView):
    serializer_class = ListSerializer
    permission_classes = [Authenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user_get_list = self.check_privilege()
        serializer = ListSerializer(user_get_list, many=True)
        log.info(f'READ: {serializer.data}')
        return Response(serializer.data)

    def check_privilege(self):
        user = self.request.user
        objs = List.objects.all()

        user_get_list = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_list):
                user_get_list.append(obj)

            elif (obj.user == user) and (obj not in user_get_list):
                user_get_list.append(obj)

            elif (str(user) in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_list):
                user_get_list.append(obj)

        return user_get_list

    def post(self, request):
        if request.user.is_authenticated:
            serializer = ListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    user=self.request.user,
                    edited_by=self.request.user,
                )
                data_s = serializer.data
                list_parent_folder = self.check_parent_folder()
                if data_s['parent_folder'] in list_parent_folder:
                    log.info(f'CREATED, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
                    return Response(data_s, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "У вас недостаточно прав."})

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

            elif (str(user) in [user.username for user in obj.authorized_users.all()]) and (obj not in parent_folder_l):
                parent_folder_l.append(obj)

        parent_folder_list = [x.id for x in parent_folder_l]
        return parent_folder_list


class ListAPIViewUpdateDeleteGet(APIView):  # odj == 'ТО ЧТО уже есть в БД' request == 'ТО что сейчас ты твоё состояние'
    serializer_class = ListSerializer
    permission_classes = [Authenticated]

    def get_object(self, pk, request):
        try:
            user = self.request.user
            obj = List.objects.get(pk=pk)
            if (obj.is_public and user.is_authenticated) or (obj.user == user)\
                    or (str(user) in [user.username for user in obj.authorized_users.all()]):
                return obj

            return False

        except List.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = List.objects.get(pk=kwargs['pk'])
            serializer = ListSerializer(instance=instance)
            log.info(f'READ, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
            return Response(serializer.data)
        except List.DoesNotExist:
            raise Http404

    def get_queryset(self):
        user = self.request.user
        objs = List.objects.all()

        user_get_list = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_list):
                user_get_list.append(obj)

            elif (obj.user == user) and (obj not in user_get_list):
                user_get_list.append(obj)

            elif (str(user) in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_list):
                user_get_list.append(obj)

        serializer = ListSerializer(user_get_list, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(pk, request)
        if obj:
            obj.delete()
            log.info(f'DELETED - "delete_folder_id": {pk}')
            return Response({"delete_list_id": pk}, status=status.HTTP_200_OK)

        return Response({"detail": "У вас недостаточно прав."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        obj = self.get_object(pk, request)
        if obj:
            serializer = ListSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save(edited_by=self.request.user)
                log.info(f'UPDATED, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "У вас недостаточно прав."})


# --------------------------Task----------------------------


class TaskAPIViewGetPost(APIView):
    serializer_class = TaskSerializer
    permission_classes = [Authenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user_get_folder = self.check_privilege()
        serializer = TaskSerializer(user_get_folder, many=True)
        log.info(f'READ: {serializer.data}')
        return Response(serializer.data)

    def check_privilege(self):
        user = self.request.user
        objs = Task.objects.all()

        user_get_task = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_task):
                user_get_task.append(obj)

            elif (obj.user == user) and (obj not in user_get_task):
                user_get_task.append(obj)

            elif (str(user) in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_task):
                user_get_task.append(obj)

        return user_get_task

    def post(self, request):
        if request.user.is_authenticated:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    user=self.request.user,
                    edited_by=self.request.user,
                )
                data_s = serializer.data
                list_parent_folder = self.check_parent_list()
                if data_s['parent_list'] in list_parent_folder:
                    log.info(f'CREATED, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
                    return Response(data_s, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "У вас недостаточно прав."})

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "У вас недостаточно прав."})

    def check_parent_list(self):
        user = self.request.user
        objs = List.objects.all()

        parent_list_l = []
        for obj in objs:
            if obj.is_public and (obj not in parent_list_l):
                parent_list_l.append(obj)

            elif (obj.user == user) and (obj not in parent_list_l):
                parent_list_l.append(obj)

            elif (str(user) in [user.username for user in obj.authorized_users.all()]) and (obj not in parent_list_l):
                parent_list_l.append(obj)

        parent_list = [x.id for x in parent_list_l]
        return parent_list


class TaskAPIViewUpdateDeleteGet(APIView):  # odj == 'ТО ЧТО уже есть в БД' request == 'ТО что сейчас ты твоё состояние'
    serializer_class = TaskSerializer
    permission_classes = [Authenticated]

    def get_object(self, pk, request):
        try:
            user = self.request.user
            obj = Task.objects.get(pk=pk)
            # log.info(user)
            # log.info(obj)
            # log.info(obj.user)
            # log.info(obj.user == user)
            # log.info(obj.is_public)
            # log.info(user.is_authenticated)
            # log.info((str(user) in [user.username for user in obj.authorized_users.all()]))
            if (obj.is_public and user.is_authenticated) or (obj.user == user)\
                    or (str(user) in [user.username for user in obj.authorized_users.all()]):
                return obj

            return False

        except Task.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = Task.objects.get(pk=kwargs['pk'])
            serializer = TaskSerializer(instance=instance)
            log.info(f'READ, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
            return Response(serializer.data)
        except Task.DoesNotExist:
            raise Http404

    def get_queryset(self):
        user = self.request.user
        objs = Task.objects.all()

        user_get_task = []
        for obj in objs:
            if obj.is_public and (obj not in user_get_task):
                user_get_task.append(obj)

            elif (obj.user == user) and (obj not in user_get_task):
                user_get_task.append(obj)

            elif (str(user) in [user.username for user in obj.authorized_users.all()]) and (obj not in user_get_task):
                user_get_task.append(obj)

        serializer = TaskSerializer(user_get_task, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(pk, request)
        if obj:
            obj.delete()
            log.info(f'DELETED - "delete_folder_id": {pk}')
            return Response({"delete_list_id": pk}, status=status.HTTP_200_OK)

        return Response({"detail": "У вас недостаточно прав."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        obj = self.get_object(pk, request)
        if obj:
            serializer = TaskSerializer(obj, data=request.data)
            log.info(serializer)
            if serializer.is_valid():
                serializer.save(edited_by=self.request.user)
                log.info(f'UPDATED, ID {serializer.data["id"]}, ID_USER {serializer.data["user"]}: {serializer.data}')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "У вас недостаточно прав."})
