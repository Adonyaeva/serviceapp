from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import service
from .models import speciality


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
        model = speciality
        fields = ('name', 'description')


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    type = SpecialitySerializer()

    class Meta:
        model = service
        depth = 1
        fields = ('name', 'description', 'estimate', 'type')
