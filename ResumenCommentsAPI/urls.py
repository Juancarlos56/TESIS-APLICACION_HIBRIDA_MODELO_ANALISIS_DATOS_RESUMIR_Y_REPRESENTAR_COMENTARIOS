from django.urls import include, path
from rest_framework import routers

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]