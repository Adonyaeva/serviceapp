from django.conf.urls import url, include
from rest_framework import generics
from service.serializers import ServiceSerializer
from service.views.ticket_list import TicketsListAPIView
from service.models import Service
from service.views import (
    address,
    ticket,
    engineer
)

urlpatterns = [
    url(r'^api/street/$', address.GetStreetListAPIView.as_view(), name='get_street_list'),
    url(r'^api/houses/$', address.GetHousesListAPIView.as_view(), name='get_houses_list'),
    url(r'^api/flats/$', address.GetFlatsListAPIView.as_view(), name='get_flats_list'),
    url(r'^api/ticket/$', ticket.TicketAPIView.as_view(), name='ticket'),
    url(r'^api/services/$', generics.ListCreateAPIView.as_view(queryset=Service.objects.all(),
        serializer_class=ServiceSerializer),
        name='service-list'),
    # url(r'^api/tickets/$', TicketsListAPIView.as_view(), name='get_ticket_list'),
    url(r'^api/engineer/$', engineer.EngineerTimeAPIView.as_view(), name='engineer'),
]
