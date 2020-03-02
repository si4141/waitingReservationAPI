from django.contrib import admin
from .models import User, ReservationSlot, Reservation


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['user_id', 'display_name', 'created_at']
    readonly_fields = ('user_id', 'display_name', 'created_at')


class ReservationSlotAdmin(admin.ModelAdmin):
    fields = ['start_time', 'available_slot']
    readonly_fields = ('available_slot', )
    list_display = ('start_time', 'available_slot')

    ordering = ('start_time', )


admin.site.register(User, UserAdmin)
admin.site.register(ReservationSlot, ReservationSlotAdmin)
admin.site.register(Reservation)
