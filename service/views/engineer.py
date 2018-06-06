from datetime import datetime, timedelta, time
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from service.serializers import EngineerSerializer
from service.models import (
    Engineer,
)


class EngineerTimeAPIView(APIView):
    """
    API endpoint that allows engineer time to be viewed.
    """
    def get(self, request):
        req_date = request.GET.get('date')
        if req_date:
            time_slot_date = datetime.strptime(req_date, "%Y-%m-%dT%H:%M:%S")
            try:
                data = Engineer.objects.filter(
                    time_slots__from_date__lte=time_slot_date,
                    time_slots__to_date__gt=time_slot_date,
                    time_slots__available=True
                )

                serialized_masters = EngineerSerializer(data, many=True)
                resp_data = JSONRenderer().render({'engineer_list': serialized_masters.data})
                return Response(resp_data, status=status.HTTP_200_OK)
            except Engineer.DoesNotExist:
                return Response({'message': 'No such date'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please, specify date'}, status=status.HTTP_400_BAD_REQUEST)
