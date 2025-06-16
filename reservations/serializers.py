# reservations/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Room, Reservation

User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'room', 'start_time', 'end_time', 'status', 'date']
        read_only_fields = ['id', 'user', 'status']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active']
