from django.contrib import admin
from .models import (
    Address,
    TimeSlot,
    Ticket,
    Engineer,
    Service,
    Speciality
)

admin.site.register(Address)
admin.site.register(TimeSlot)
admin.site.register(Ticket)
admin.site.register(Engineer)
admin.site.register(Service)
admin.site.register(Speciality)

