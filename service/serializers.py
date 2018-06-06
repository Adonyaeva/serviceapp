from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import (
    Service,
    Speciality,
    Ticket,
    Address,
    TimeSlot,
    Engineer,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ('name', 'description')


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    type = SpecialitySerializer()

    class Meta:
        model = Service
        depth = 1
        fields = ('id', 'name', 'description', 'estimate', 'type')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street_name', 'house_id', 'house_number', 'flat_id', 'flat_number')


class EngineerSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer()

    class Meta:
        model = Engineer
        fields = ('id', 'name_full', 'name_short', 'speciality')


class TimeSlotSerializer(serializers.ModelSerializer):
    master = EngineerSerializer()

    class Meta:
        model = TimeSlot
        fields = ('id', 'from_date', 'to_date', 'available', 'master')


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer()
    service = ServiceSerializer()
    time_slot = TimeSlotSerializer()
    speciality = SpecialitySerializer()
    engineer = EngineerSerializer()

    class Meta:
        model = Ticket
        depth = 1
        fields = ('id', 'created_time', 'comment', 'address', 'service', 'status_id', 'status_updated_time', 'time_slot',
                  'speciality', 'spent_time', 'engineer')
