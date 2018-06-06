from datetime import datetime, timedelta, time
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from service.serializers import TimeSlotSerializer
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
            time_slot_date = datetime.strptime(req_date, "%Y-%m-%dT%H:%M:%S")
            try:
                data = TimeSlot.objects.filter(
                    from_date__lte=time_slot_date,
                    to_date__gte=time_slot_date,
                    available=True,
                )

                serialized_timeslots = TimeSlotSerializer(data, many=True)
                resp_data = JSONRenderer().render(serialized_timeslots.data)
                return Response(resp_data, status=status.HTTP_200_OK)
            except TimeSlot.DoesNotExist:
                return Response({'message': 'No such date'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please, specify date'}, status=status.HTTP_400_BAD_REQUEST)
