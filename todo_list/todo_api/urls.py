import logging

from django.urls import path, include
from rest_framework import routers

from .views import FolderAPIList, ListAPIList, TaskAPIList, V1APIView, TaskAPIRetrieveUpdateDestroy, \
    ListAPIRetrieveUpdateDestroy, FolderAPIRetrieveUpdateDestroy

# from .views import FolderViewSet, ListViewSet, TaskViewSet
# router = routers.DefaultRouter()
# router.register("folders", FolderViewSet)  # http://127.0.0.1:8000/api/v1/folders/ + <int:pk>/
# router.register("lists", ListViewSet)  # http://127.0.0.1:8000/api/v1/lists/ + <int:pk>/
# router.register("tasks", TaskViewSet)  # http://127.0.0.1:8000/api/v1/tasks/ + <int:pk>/
# logging.info(router.urls)
#
# urlpatterns = [
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path("", V1APIView.as_view()),
    path("folders/", FolderAPIList.as_view()),
    path("folders/<int:pk>/", FolderAPIRetrieveUpdateDestroy.as_view()),
    path("lists/", ListAPIList.as_view()),
    path("lists/<int:pk>/", ListAPIRetrieveUpdateDestroy.as_view()),
    path("tasks/", TaskAPIList.as_view()),
    path("tasks/<int:pk>/", TaskAPIRetrieveUpdateDestroy.as_view()),
]
