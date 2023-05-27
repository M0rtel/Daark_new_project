import logging

from django.urls import path, include
from rest_framework import routers

from .views import V1APIView, FolderAPIViewGetPost, FolderAPIViewUpdateDeleteGet, ListAPIViewGetPost, \
    ListAPIViewUpdateDeleteGet

# from .views import FolderAPIList, V1APIView, FolderAPIRetrieveUpdateDestroy

# from .views import FolderViewSet, ListViewSet, TaskViewSet
# router = routers.DefaultRouter()
# router.register("folders", FolderViewSet)  # http://127.0.0.1:8000/api/v1/folders/ + <int:pk>/
# router.register("lists", ListViewSet)  # http://127.0.0.1:8000/api/v1/lists/ + <int:pk>/
# router.register("tasks", TaskViewSet)  # http://127.0.0.1:8000/api/v1/tasks/ + <int:pk>/
# logging.info(router.urls)
#
# urlpatterns = [
#     path("", V1APIView.as_view()),
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path("", V1APIView.as_view()),
    path('folders/', FolderAPIViewGetPost.as_view(), name='folders-list'),
    path('folders/<int:pk>/', FolderAPIViewUpdateDeleteGet.as_view(), name='folders-detail'),
    path("lists/", ListAPIViewGetPost.as_view()),
    path("lists/<int:pk>/", ListAPIViewUpdateDeleteGet.as_view()),
    # path("tasks/", TaskAPIList.as_view()),
    # path("tasks/<int:pk>/", TaskAPIRetrieveUpdateDestroy.as_view()),
]



