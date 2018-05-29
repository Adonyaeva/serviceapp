from django.db import models
from django.utils import timezone


class Address(models.Model):
    street_name = models.CharField(max_length=200)
    house_id = models.IntegerField()
    house_number = models.IntegerField()
    flat_number = models.IntegerField()
    flat_id = models.IntegerField()


    def __str__(self):
        return self.street_name + self.house_number + self.flat_number


class TimeSlot(models.Model):
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    available = models.BooleanField()


    def __str__(self):
        return self.from_date + self.to_date


class Ticket(models.Model):
    created_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    address = models.ForeignKey('service.Address', on_delete=models.CASCADE)
    service = models.ForeignKey('service.Service', on_delete=models.CASCADE)
    status_id = models.IntegerField()
    status_updated_time = models.DateTimeField()
    time_slot = models.ForeignKey('service.TimeSlot', on_delete=models.DO_NOTHING)
    speciality = models.CharField(max_length=200)
    engineer = models.ForeignKey('service.Engineer', on_delete=models.DO_NOTHING)
    spent_time = models.IntegerField()

    def __str__(self):
        return self.address + self.service + self.time_slot


class Engineer(models.Model):
    name_full = models.CharField(max_length=400)
    name_short = models.CharField(max_length=100)
    speciality = models.CharField(max_length=200)
    time_slots = models.ManyToManyField('service.TimeSlot')


    def __str__(self):
        return self.name_full


class Service(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    estimate = models.IntegerField()
    type = models.ForeignKey('service.Speciality', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()

    def __str__(self):
        return self.name

