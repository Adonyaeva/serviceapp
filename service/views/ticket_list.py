import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from service.models import (
    Address,
    TimeSlot,
    Ticket,
    Engineer,
    Service,
    Speciality
)


class TicketsListAPIView(APIView):
    """
    API endpoint that allows ticket list to be viewed.
    """

    def get(self, request):
        ticket_status = request.GET.get('status', '') or ''
        ticket_date = request.GET.get('date', '') or ''
        filter_params = {}
        if ticket_status:
            filter_params['status'] = ticket_status
        if ticket_date:
            filter_params['time_slot'] = ticket_date
        try:
            data = Ticket.objects.filter(filter_params)
            data = json.dumps(data)
            return Response(data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'message': 'Tickets have not been found'}, status=status.HTTP_400_BAD_REQUEST)
