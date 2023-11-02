"""
URL configuration for NotificationService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from mailing import views

# The code block is creating a router object using the `DefaultRouter` class from the `rest_framework.routers` module.
router = routers.DefaultRouter()
router.register(r'mailing', views.MailingViewset)
router.register(r'client', views.ClientViewset)
router.register(r'message', views.MessageViewest)
router.register(r'timezone', views.SetTimeZoneViewset)

# The `schema_view` variable is creating a schema view for the API documentation using the `get_schema_view`
# function from the `drf_yasg` package.
schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API of notification service",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('allauth.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]