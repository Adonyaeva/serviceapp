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


class TicketAPIView(APIView):
    """
    API endpoint that allows tickets to be viewed and created.
    """

    def get(self, request):
        ticket_id = int(request.GET['id']) if request.GET.get('id') else 0
        if ticket_id:
            try:
                data = Ticket.objects.get(id=ticket_id)
                return Response(data, status=status.HTTP_200_OK)
            except Ticket.DoesNotExist:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please, specify id'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        ticket_comment = request.POST.get('comment', '') or ''
        ticket_address = request.POST.get('address', {}) or {}
        ticket_service = request.POST.get('service', {}) or {}
        ticket_status_id = request.POST.get('status_id', '') or ''
        ticket_time_slot = request.POST.get('time_slot', {}) or {}
        ticket_speciality = request.POST.get('speciality', '') or ''
        ticket_engineer = request.POST.get('engineer', {}) or {}
        ticket_spent_time = request.POST.get('spent_time', '') or ''
        if not (ticket_address and ticket_service and ticket_time_slot and ticket_engineer and ticket_speciality):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        address = Address.objects.get_or_create(
            street_name=ticket_address['street_name'],
            house_id=ticket_address['house_id'],
            house_number=ticket_address['house_number'],
            flat_number=ticket_address['flat_number'],
            flat_id=ticket_address['flat_id']
        )

        try:
            service = Service.objects.get(name=ticket_service['name'])
        except Service.DoesNotExist:
            return Response({'message': 'Incorrect service'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            engineer = Engineer.objects.get(name=ticket_engineer['name_full'],
                                            speciality=ticket_engineer['speciality'])
        except Engineer.DoesNotExist:
            return Response({'message': 'Incorrect Engineer'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            speciality = Speciality.objects.get(name=ticket_speciality['name'])
        except Speciality.DoesNotExist:
            return Response({'message': 'Incorrect Speciality'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            time_slot = TimeSlot.objects.get(id=ticket_time_slot['id'])
        except TimeSlot.DoesNotExist:
            return Response({'message': 'Incorrect TimeSlot'}, status=status.HTTP_400_BAD_REQUEST)

        ticket_id = Ticket.objects.create(
            comment=ticket_comment,
            address=address,
            service=service,
            status_id=ticket_status_id,
            time_slot=time_slot,
            speciality=speciality,
            engineer=engineer,
            spent_time=ticket_spent_time
        )

        return Response({Ticket.objects.get(id=ticket_id)}, status=status.HTTP_200_OK)

    def put(self, request):
        ticket_id = request.POST.get('id', '') or ''
        if not ticket_id:
            return Response({'message': 'Please, specify id'}, status=status.HTTP_400_BAD_REQUEST)
        ticket = Ticket.objects.get(id=ticket_id)
