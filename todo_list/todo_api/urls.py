import logging

from django.urls import path

from .views import V1APIView, FolderAPIViewGetPost, FolderAPIViewUpdateDeleteGet, ListAPIViewGetPost, \
    ListAPIViewUpdateDeleteGet, LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView


urlpatterns = [
    path("", V1APIView.as_view()),
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('folders/', FolderAPIViewGetPost.as_view(), name='folders-list'),
    path('folders/<int:pk>/', FolderAPIViewUpdateDeleteGet.as_view(), name='folders-detail'),
    path("lists/", ListAPIViewGetPost.as_view()),
    path("lists/<int:pk>/", ListAPIViewUpdateDeleteGet.as_view()),
    # path("tasks/", TaskAPIList.as_view()),
    # path("tasks/<int:pk>/", TaskAPIRetrieveUpdateDestroy.as_view()),
]



