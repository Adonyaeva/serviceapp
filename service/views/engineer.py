# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from service.models import (
#     Address,
#     TimeSlot,
#     Ticket,
#     Engineer,
#     Service,
#     Speciality
# )
#
#
# class EngineerTimeAPIView(APIView):
#     """
#     API endpoint that allows engineer time to be viewed.
#     """
#     def get(self, request):
#         date = request.GET.get('date')
#         if date:
#             try:
#                 data = Engineer.objects.get(time_slots=date)
#                 return Response(data, status=status.HTTP_200_OK)
#             except Engineer.DoesNotExist:
#                 return Response({'message': 'No such date'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'message': 'Please, specify date'}, status=status.HTTP_400_BAD_REQUEST)