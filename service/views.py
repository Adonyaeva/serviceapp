from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from service.serializers import (
    UserSerializer,
    GroupSerializer
)
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from urllib.request import urlopen, URLError
from serviceapp.settings import API_ADDRESS_SERVER_SETTINGS
import requests
from rest_framework.response import Response
from .models import (
    Address,
    TimeSlot,
    Ticket,
    Engineer,
    Service,
    Speciality
)
import json


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


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


class GetStreetListAPIView(APIView):
    """
    API endpoint that allows to get list of streets.
    """

    @cache_page(CACHE_TTL)
    def get(self, request):
        url = API_ADDRESS_SERVER_SETTINGS['URL_STREET'] + '?id=' + request.GET['id'] if request.GET.get('id') else \
            API_ADDRESS_SERVER_SETTINGS['URL_STREET']
        try:
            result = requests.get(url, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                             API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
            data = result.content
            status_code = status.HTTP_200_OK
        except URLError as e:
            data = e
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data, status=status_code)


class GetHousesListAPIView(APIView):
    """
    API endpoint that allows to get list of houses.
    """
    @cache_page(CACHE_TTL)
    def get(self, request):
        url = API_ADDRESS_SERVER_SETTINGS['URL_HOUSE'] + '?street=' + request.GET['street_id']
        try:
            result = requests.get(url, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                             API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
            data = result.content
            status_code = status.HTTP_200_OK
        except URLError as e:
            data = e
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data, status=status_code)


class GetFlatsListAPIView(APIView):
    """
    API endpoint that allows users to get list of flats with services.
    """
    @cache_page(CACHE_TTL)
    def get(self, request):
        url = API_ADDRESS_SERVER_SETTINGS['URL_FLAT'] + '?house=' + request.GET['house_id']
        try:
            result = requests.get(url, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                             API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
            flats = json.loads(result.content)
            response_data = []
            # Getting services to flats
            for flat in flats:
                try:
                    flat_address = Address.objects.get(flat_id=flat['id'], house_id=flat['house'])
                    flat_tickets = Ticket.objects.filter(address=flat_address)
                    flat['services'] = []
                    for flat_ticket in flat_tickets:
                        flat_service = {
                            'name': flat_ticket.service.name,
                            'description': flat_ticket.service.description,
                            'estimate': flat_ticket.service.estimate,
                            'type': str(flat_ticket.service.type),
                        }
                        flat['services'].append(flat_service)

                except ObjectDoesNotExist:
                    pass
                response_data.append(flat)
            status_code = status.HTTP_200_OK
        except URLError as e:
            response_data = e
            status_code = status.HTTP_400_BAD_REQUEST
        response_data = json.dumps(response_data)
        return Response(response_data, status=status_code)


class TicketAPIView(APIView):
    """
    API endpoint that allows tickets to be viewed and created.
    """
    @cache_page(CACHE_TTL)
    def get(self, request):
        ticket_id = int(request.GET['id']) if request.GET.get('id') else 0
        if ticket_id > 0:
            try:
                data = Ticket.objects.get(pk=ticket_id)
                return Response(data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'Incorrect id'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Please, specify id'}, status=status.HTTP_400_BAD_REQUEST)

    @cache_page(CACHE_TTL)
    def post(self, request):
        ticket_comment = request.POST['comment'] if request.POST.get('comment') else ''
        ticket_address = request.POST['address']
        ticket_service = request.POST['service']
        ticket_status_id = request.POST['status_id']
        ticket_time_slot = request.POST['time_slot']
        ticket_speciality = request.POST['speciality']
        ticket_engineer = request.POST['engineer']
        ticket_spent_time = request.POST['spent_time']
        if len(ticket_address) > 0 and len(ticket_service) > 0 and len(ticket_time_slot) > 0 and len(ticket_engineer) \
                > 0 and len(ticket_speciality) > 0:
            address = Address.objects.get(
                street_name=ticket_address['street_name'],
                house_id=ticket_address['house_id'],
                house_number=ticket_address['house_number'],
                flat_number=ticket_address['flat_number'],
                flat_id=ticket_address['flat_id'])
            if not hasattr(address, 'id'):
                try:
                    address = Address.objects.create(
                        street_name=ticket_address['street_name'],
                        house_id=ticket_address['house_id'],
                        house_number=ticket_address['house_number'],
                        flat_number=ticket_address['flat_number'],
                        flat_id=ticket_address['flat_id'])
                except ObjectDoesNotExist:
                    return Response({'Incorrect Address'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                service = Service.objects.get(name=ticket_service['name'])
            except ObjectDoesNotExist:
                return Response({'Incorrect Service'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                engineer = Engineer.objects.get(name=ticket_engineer['name_full'], speciality=ticket_engineer['speciality'])
            except ObjectDoesNotExist:
                return Response({'Incorrect Engineer'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                speciality = Speciality.objects.get(name=ticket_speciality['name'])
            except ObjectDoesNotExist:
                return Response({'Incorrect Speciality'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                time_slot = TimeSlot.objects.get(pk=ticket_time_slot['id'])
            except ObjectDoesNotExist:
                return Response({'Incorrect TimeSlot'}, status=status.HTTP_400_BAD_REQUEST)

            ticket_id = Ticket.objects.create(comment=ticket_comment, address=address, service=service,
                                              status_id=ticket_status_id, time_slot=time_slot,
                                              speciality=speciality, engineer=engineer,
                                              spent_time=ticket_spent_time)

            return Response({Ticket.objects.get(id=ticket_id)}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

