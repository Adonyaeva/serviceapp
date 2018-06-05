from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    street_name = models.CharField(max_length=200)
    house_id = models.IntegerField()
    house_number = models.IntegerField()
    flat_number = models.IntegerField()
    flat_id = models.IntegerField()

    def __str__(self):
        return str(self.street_name) + '_' + str(self.house_number) + '_' + str(self.flat_number)


class TimeSlot(models.Model):
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    available = models.BooleanField()
    master = models.ForeignKey('service.Engineer', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.from_date) + '_' + str(self.to_date)


class Ticket(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    address = models.ForeignKey('service.Address', on_delete=models.CASCADE)
    service = models.ForeignKey('service.Service', on_delete=models.CASCADE)
    status_id = models.IntegerField(default=0)
    status_updated_time = models.DateTimeField(auto_now=True)
    time_slot = models.ForeignKey('service.TimeSlot', on_delete=models.DO_NOTHING)
    speciality = models.ForeignKey('service.Speciality', on_delete=models.DO_NOTHING)
    engineer = models.ForeignKey('service.Engineer', on_delete=models.DO_NOTHING)
    spent_time = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='ticket')

    def __str__(self):
        return str(self.address) + '_' + str(self.service) + '_' + str(self.time_slot)


class Engineer(models.Model):
    name_full = models.CharField(max_length=400)
    name_short = models.CharField(max_length=100)
    speciality = models.ForeignKey('service.Speciality', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name_full


class Service(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    estimate = models.IntegerField()
    type = models.ForeignKey('service.Speciality', on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='services')

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# class TimeSlotToEngineer(models.Model):
#     time_slot_id = models.IntegerField()
#     engineer_id = models.IntegerField()
#
#     def __str__(self):
#         return str(self.time_slot_id) + '_' + str(self.engineer_id)
