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


if not ReservationSlot.objects.exists():
    import datetime
    jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')
    start_times = []
    start = datetime.datetime(2020, 4, 25, 10, 00, tzinfo=jst)
    while start < datetime.datetime(2020, 4, 26, 17, 0, tzinfo=jst):
        if 10 <= start.hour < 17:
            start_times.append(start)
        start += datetime.timedelta(minutes=10)

    for start in start_times:
        rs = ReservationSlot(start_time=start)
        rs.save()