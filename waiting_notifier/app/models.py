from django.db import models
from django.utils.timezone import localtime


# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    display_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


class ReservationSlot(models.Model):
    start_time = models.DateTimeField(primary_key=True)
    available_slot = models.IntegerField(default=8)

    def __str__(self):
        return f'{localtime(self.start_time): %Y-%m-%d %H:%M:%S}'


class Reservation(models.Model):
    reservation_slot = models.ForeignKey(ReservationSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
