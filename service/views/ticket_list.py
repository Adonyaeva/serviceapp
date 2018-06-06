from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from service.serializers import TicketSerializer
from service.models import Ticket


class TicketsListAPIView(APIView):
    """
    API endpoint that allows ticket list to be viewed.
    """

    def get(self, request):
        params = {}
        ticket_status = request.GET.get('status', '') or ''
        if ticket_status:
            params['status_id'] = ticket_status
        ticket_date = request.GET.get('date', '') or ''
        if ticket_date:
            params['time_slot__from_date__lte'] = ticket_date
            params['time_slot__to_date__gte'] = ticket_date
        ticket_house = request.GET.get('house', '') or ''
        if ticket_house:
            params['address__house_id'] = ticket_house

        try:
            data = Ticket.objects.filter(**params)

            serialized_tickets = TicketSerializer(data, many=True)
            resp_data = JSONRenderer().render(serialized_tickets.data)
            return Response(resp_data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'message': 'Tickets have not been found'}, status=status.HTTP_400_BAD_REQUEST)
