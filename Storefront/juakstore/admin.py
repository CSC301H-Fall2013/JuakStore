from django.contrib import admin
from juakstore import models

admin.site.register(models.Booking)
admin.site.register(models.BookingCategory)
admin.site.register(models.ClientBooking)
admin.site.register(models.Room)
admin.site.register(models.Partner)