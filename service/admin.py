from django.contrib import admin
from .models import address
from .models import timeslot
from .models import ticket
from .models import engineer
from .models import service

admin.site.register(address)
admin.site.register(timeslot)
admin.site.register(ticket)
admin.site.register(engineer)
admin.site.register(service)

