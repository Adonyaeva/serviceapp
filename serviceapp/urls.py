"""serviceapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from service import views
from rest_framework import generics
from service.serializers import ServiceSerializer
from service.models import Service


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/login/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    url(r'^api/services/$', generics.ListCreateAPIView.as_view(queryset=Service.objects.all(),
                                                           serializer_class=ServiceSerializer), name='service-list'),
    url(r'^api/street/$', views.GetStreetListAPIView.as_view(), name='get_street_list'),
    url(r'^api/houses/$', views.GetHousesListAPIView.as_view(), name='get_houses_list'),
    url(r'^api/flats/$', views.GetFlatsListAPIView.as_view(), name='get_flats_list'),
    url(r'^api/ticket/$', views.TicketAPIView.as_view(), name='get_ticket'),
]
