from rest_framework import serializers
from .models import User, ReservationSlot, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'display_name', 'created_at')


class ReservationSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationSlot
        fields = ('start_time', 'available_slot')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields =('reservation_slot', 'user', 'create_at')
