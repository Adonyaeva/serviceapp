from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from service.serializers import UserSerializer, GroupSerializer
from urllib.request import urlopen, URLError
from serviceapp.settings import API_ADDRESS_SERVER_SETTINGS
import requests
from django.http import HttpResponse


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def get_street_list(request):
    response = HttpResponse()
    url = API_ADDRESS_SERVER_SETTINGS['URL_STREET'] + '?id=' + request.GET['id'] if hasattr(request, 'id') else \
        API_ADDRESS_SERVER_SETTINGS['URL_STREET']
    try:
        result = requests.get(url, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                         API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
        response.content = result.content
        response.status_code = 200
    except URLError:
        response.status_code = 403
    return response


def get_houses_list(request):
    response = HttpResponse()
    url = API_ADDRESS_SERVER_SETTINGS['URL_HOUSE'] + '?street=' + request.GET['street_id']
    try:
        result = requests.get(url, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                         API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
        response.content = result.content
        response.status_code = 200
    except URLError:
        response.status_code = 403
    return response


def get_flats_list(request):
    response = HttpResponse()
    url = API_ADDRESS_SERVER_SETTINGS['URL_FLAT'] + '?house=' + request.GET['house_id']
    try:
        result = requests.get(url, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                         API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
        response.content = result.content
        response.status_code = 200
    except URLError:
        response.status_code = 403
    return response
