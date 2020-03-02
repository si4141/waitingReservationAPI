from rest_framework import serializers
from .models import User, ReservationSlot, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'display_name', 'created_at')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('reservation_slot', 'user', 'create_at')


class ReservationSlotSerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = ReservationSlot
        fields = ('start_time', 'available_slot', 'reservations', 'remaining')

    def get_reservations(self, obj):
        try:
            reservations_abstract_contents = ReservationSerializer(
                Reservation.objects.all().filter(
                    reservation_slot=ReservationSlot.objects.get(start_time=obj.start_time)
                ),
                many=True
            ).data
            return reservations_abstract_contents
        except Reservation.DoesNotExist:
            reservations_abstract_contents = None
            return reservations_abstract_contents

    def get_remaining(self, obj):
        try:
            num_reservations = Reservation.objects.all().filter(
                reservation_slot=ReservationSlot.objects.get(start_time=obj.start_time)
            ).count()
            return obj.available_slot - num_reservations
        except Reservation.DoesNotExist:
            return obj.available_slot
