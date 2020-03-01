from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    display_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


class ReservationSlot(models.Model):
    start_time = models.DateTimeField()
    available_slot = models.IntegerField(default=10)


class Reservation(models.Model):
    reservation_slot = models.ForeignKey(ReservationSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
