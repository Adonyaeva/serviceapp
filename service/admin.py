from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import (
    Address,
    TimeSlot,
    Ticket,
    Engineer,
    Service,
    Speciality
)


class TimeSlotAdmin(ModelAdmin):
    list_display = ['from_date', 'to_date', 'available', 'engineer']

    list_filter = (
        'engineer',
    )

    # search_fields = (
    #     'msisdn',
    # )


admin.site.register(Address)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(Ticket)
admin.site.register(Engineer)
admin.site.register(Service)
admin.site.register(Speciality)

