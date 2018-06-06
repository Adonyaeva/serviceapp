import json
from django.core import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from service.utils.get_or_create_adress import get_or_create_adress
from service.models import (
    TimeSlot,
    Ticket,
    Engineer,
    Service,
    Speciality
)
from service.tasks import send_status_email


class TicketAPIView(APIView):
    """
    API endpoint that allows tickets to be viewed and created.
    """

    def get(self, request):
        ticket_id = request.GET.get('id', '') or ''
        if ticket_id:
            try:
                data = Ticket.objects.get(id=int(ticket_id))
                resp_data = serializers.serialize('json', [data])
                resp_data = json.loads(resp_data)
                resp_data = json.dumps(resp_data)
                return Response(resp_data, status=status.HTTP_200_OK)
            except Ticket.DoesNotExist:
                return Response({'message': 'No ticket with such id.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please, specify id'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        ticket_comment = request.data.get('comment', '') or ''
        ticket_address = request.data.get('address', {}) or {}
        ticket_service = request.data.get('service', {}) or {}
        ticket_status_id = request.data.get('status_id', 1) or 1
        ticket_time_slot = request.data.get('time_slot', {}) or {}
        ticket_speciality = request.data.get('speciality', {}) or {}
        ticket_engineer = request.data.get('engineer', {}) or {}
        ticket_spent_time = request.data.get('spent_time', 0) or 0

        if not (ticket_address and ticket_service and ticket_time_slot and ticket_engineer and ticket_speciality):
            return Response({'message': 'Not all required fields are specified!'}, status=status.HTTP_400_BAD_REQUEST)

        address = get_or_create_adress(ticket_address)

        try:
            service = Service.objects.get(id=ticket_service['id'])
        except Service.DoesNotExist:
            return Response({'message': 'Incorrect service'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            engineer = Engineer.objects.get(id=ticket_engineer['id'])
        except Engineer.DoesNotExist:
            return Response({'message': 'Incorrect Engineer'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            speciality = Speciality.objects.get(id=ticket_speciality['id'])
        except Speciality.DoesNotExist:
            return Response({'message': 'Incorrect Speciality'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            time_slot = TimeSlot.objects.get(id=ticket_time_slot['id'])
        except TimeSlot.DoesNotExist:
            return Response({'message': 'Incorrect TimeSlot'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket = Ticket.objects.create(
                comment=ticket_comment,
                address=address[0],
                service=service,
                status_id=ticket_status_id,
                time_slot=time_slot,
                speciality=speciality,
                engineer=engineer,
                spent_time=ticket_spent_time
            )

            resp_data = serializers.serialize('json', [ticket])
            resp_data = json.loads(resp_data)
            resp_data = json.dumps(resp_data)
            status_code = status.HTTP_200_OK
        except:
            resp_data = {'message': 'Can not create ticket'}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp_data, status=status_code)

    def put(self, request):
        ticket_id = request.data.get('id', '') or ''
        if not ticket_id:
            return Response({'message': 'Please, specify id'}, status=status.HTTP_400_BAD_REQUEST)
        ticket_comment = request.data.get('comment', '') or ''
        ticket_address = request.data.get('address', {}) or {}
        ticket_service = request.data.get('service', {}) or {}
        ticket_status_id = request.data.get('status_id', 1) or 1
        ticket_time_slot = request.data.get('time_slot', {}) or {}
        ticket_speciality = request.data.get('speciality', {}) or {}
        ticket_engineer = request.data.get('engineer', {}) or {}
        ticket_spent_time = request.data.get('spent_time', 0) or 0
        if not (ticket_status_id or ticket_time_slot or ticket_engineer):
            return Response({'message': 'Not all required fields are specified!'}, status=status.HTTP_400_BAD_REQUEST)
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket_comment:
            ticket.comment = ticket_comment
        if ticket_address:
            address = get_or_create_adress(ticket_address)
            ticket.address = address
        if ticket_service:
            service = Service.objects.get(id=ticket_service['id'])
            ticket.service = service
        if ticket_time_slot:
            time_slot = TimeSlot.objects.get(id=ticket_time_slot['id'])
            ticket.time_slot = time_slot
        if ticket_status_id:
            ticket.status_id = ticket_status_id
            send_status_email.delay(ticket_id)
        if ticket_speciality:
            speciality = Speciality.objects.get(id=ticket_speciality['id'])
            ticket.speciality = speciality
        if ticket_engineer:
            engineer = Engineer.objects.get(id=ticket_engineer['id'])
            ticket.engineer = engineer
        if ticket_spent_time:
            ticket.spent_time = ticket_spent_time
        try:
            ticket.save()
            resp_data = serializers.serialize('json', [ticket])
            resp_data = json.loads(resp_data)
            resp_data = json.dumps(resp_data)
            status_code = status.HTTP_200_OK
        except:
            resp_data = {'message': 'Can not create ticket'}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(resp_data, status=status_code)
