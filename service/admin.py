from django.contrib import admin
from .models import address
from .models import timeslot
from .models import ticket
from .models import engineer
from .models import service
from .models import speciality

admin.site.register(address)
admin.site.register(timeslot)
admin.site.register(ticket)
admin.site.register(engineer)
admin.site.register(service)
admin.site.register(speciality)

