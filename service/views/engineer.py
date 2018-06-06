import json
from datetime import datetime, timedelta, time
from rest_framework.views import APIView
from django.core import serializers
from rest_framework import status
from rest_framework.response import Response
from service.models import (
    TimeSlot,
    Engineer,
)


class EngineerTimeAPIView(APIView):
    """
    API endpoint that allows engineer time to be viewed.
    """
    def get(self, request):
        req_date = request.GET.get('date')
        if req_date:
            time_slot_date = datetime.strptime(req_date, "%Y-%m-%dT%H:%M:%S").date()
            f = open('text.txt', 'w')
            f.write(str(time_slot_date))
            f.close()
            try:
                data = TimeSlot.objects\
                    .filter(from_date__lte=time_slot_date)\
                    .filter(to_date__gte=time_slot_date)
                response_data = []
                # for time_slot in data:
                #     response_data.append(time_slot['master'])

                resp_data = serializers.serialize('json', data)
                resp_data = json.loads(resp_data)
                resp_data = json.dumps(resp_data)
                return Response(resp_data, status=status.HTTP_200_OK)
            except TimeSlot.DoesNotExist:
                return Response({'message': 'No such date'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please, specify date'}, status=status.HTTP_400_BAD_REQUEST)
