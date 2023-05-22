from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include('todo_api.urls')),
    path("api/v1/auth/", include('djoser.urls')),  # djoser
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # TJW
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # TJW
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # TJW
]
