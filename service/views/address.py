from rest_framework.views import APIView
from rest_framework import status
import json
from service.get_address import send_request

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from service.models import (
    Address,
    Ticket,
)


class GetStreetListAPIView(APIView):
    """
    API endpoint that allows to get list of streets.
    """

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
