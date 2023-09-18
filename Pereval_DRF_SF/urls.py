from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='My Django APIs',
        default_version='v1',
        description='Creating API docs was never this easy!!!',
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('pereval.urls')),
    path('docs', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc', schema_view.with_ui('swagger', cache_timeout=0)),
]
