from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from service.serializers import (
    UserSerializer,
    GroupSerializer,
    TicketSerializer
)
import json
from .get_address import send_request
#from django.core.cache.backends.base import DEFAULT_TIMEOUT
#from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from .models import (
    Address,
    TimeSlot,
    Ticket,
    Engineer,
    Service,
    Speciality
)
from .tasks import send_email

#CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


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

 #   @cache_page(CACHE_TTL)
    def get(self, request):
        result = send_request('URL_STREET', {})
        if result:
            data = result
            status_code = status.HTTP_200_OK
        else:
            data = {}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


class GetHousesListAPIView(APIView):
    """
    API endpoint that allows to get list of houses.
    """
  #  @cache_page(CACHE_TTL)
    def get(self, request):
        result = send_request('URL_HOUSE', {'street': request.GET.get('street_id')})
        if result:
            data = result
            status_code = status.HTTP_200_OK
        else:
            data = {}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


class GetFlatsListAPIView(APIView):
    """
    API endpoint that allows users to get list of flats with services.
    """
   # @cache_page(CACHE_TTL)
    def get(self, request):
        result = send_request('URL_FLAT', {'house': request.GET.get('house_id')})
        if result:
            flats = json.loads(result)
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
        else:
            response_data = {}
            status_code = status.HTTP_400_BAD_REQUEST
        response_data = json.dumps(response_data)
        return Response(response_data, status=status_code)


class TicketAPIView(APIView):
    """
    API endpoint that allows tickets to be viewed and created.
    """

    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return ''

    def get(self, request):
        ticket_id = int(request.GET['id']) if request.GET.get('id') else 0
        if ticket_id:
            try:
                data = Ticket.objects.get(id=ticket_id)
                return Response(data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        ticket_comment = request.POST['comment'] if request.POST.get('comment') else ''
        ticket_address = request.POST['address'] if request.POST.get('address') else ''
        ticket_service = request.POST['service'] if request.POST.get('service') else ''
        ticket_status_id = request.POST['status_id'] if request.POST.get('status_id') else ''
        ticket_time_slot = request.POST['time_slot'] if request.POST.get('time_slot') else ''
        ticket_speciality = request.POST['speciality'] if request.POST.get('speviality') else ''
        ticket_engineer = request.POST['engineer'] if request.POST.get('engineer') else ''
        ticket_spent_time = request.POST['spent_time'] if request.POST.get('spent_time') else ''
        if ticket_address and ticket_service and ticket_time_slot and ticket_engineer and ticket_speciality:
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
                    return Response({'message': 'Incorrect Address'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                service = Service.objects.get(name=ticket_service['name'])
            except ObjectDoesNotExist:
                return Response({'message': 'Incorrect service'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                engineer = Engineer.objects.get(name=ticket_engineer['name_full'], speciality=ticket_engineer['speciality'])
            except ObjectDoesNotExist:
                return Response({'message': 'Incorrect Engineer'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                speciality = Speciality.objects.get(name=ticket_speciality['name'])
            except ObjectDoesNotExist:
                return Response({'message': 'Incorrect Speciality'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                time_slot = TimeSlot.objects.get(id=ticket_time_slot['id'])
            except ObjectDoesNotExist:
                return Response({'message': 'Incorrect TimeSlot'}, status=status.HTTP_400_BAD_REQUEST)

            ticket_id = Ticket.objects.create(comment=ticket_comment, address=address, service=service,
                                              status_id=ticket_status_id, time_slot=time_slot,
                                              speciality=speciality, engineer=engineer,
                                              spent_time=ticket_spent_time)

            return Response({Ticket.objects.get(id=ticket_id)}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        ticket = self.get_object(pk)
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketsListAPIView(APIView):
    """
    API endpoint that allows ticket list to be viewed.
    """
    def get(self, request):
        ticket_status = request.GET.get('status')
        ticket_date = request.GET.get('date')
        filter_params = {}
        if ticket_status:
            filter_params['status'] = ticket_status
        if ticket_date:
            filter_params['time_slot'] = ticket_date
        try:
            data = Ticket.objects.filter(filter_params)
            data = json.dumps(data)
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class EngineerTimeAPIView(APIView):
    """
    API endpoint that allows engineer time to be viewed.
    """
    def get(self, request):
        date = request.GET.get('date')
        if date:
            try:
                data = Engineer.objects.get(time_slots=date)
                return Response(data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'message': 'No such date'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please, specify date'}, status=status.HTTP_400_BAD_REQUEST)

