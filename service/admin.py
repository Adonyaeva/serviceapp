from django.contrib import admin
from .models import Address
from .models import TimeSlot
from .models import Ticket
from .models import Engineer
from .models import Service

admin.site.register(Address)
admin.site.register(TimeSlot)
admin.site.register(Ticket)
admin.site.register(Engineer)
admin.site.register(Service)

