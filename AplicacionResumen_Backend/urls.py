"""AplicacionResumen_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


### Visualizacion de nuestra API, mediante documentacion con swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Cocoments API",
      default_version='v1',
      description="Api Rest para resumen y representación de comentarios sobre bares y restaurantes",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jbarrerab1@est.ups.edu.ec"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   ##Permisos de nuestra aplicacion
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ResumenCommentsAPI.urls')),
    path('documentacion/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
