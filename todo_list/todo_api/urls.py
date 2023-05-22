import logging

from django.urls import path, include
from rest_framework import routers

from .views import FolderViewSet, ListViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register("folders", FolderViewSet)
router.register("lists", ListViewSet)
router.register("tasks", TaskViewSet)
logging.info(router.urls)


urlpatterns = [
    path("", include(router.urls)),  # http://127.0.0.1:8000/api/v1/folder/
]
