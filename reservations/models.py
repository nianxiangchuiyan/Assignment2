# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Room(models.Model):
    """
    The Room model represents a conference room in the system.
    Attributes like name, location, capacity, and description help
    identify and detail the room.
    """
    name = models.CharField(max_length=100, help_text="Room name")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Room location")
    capacity = models.IntegerField(help_text="Maximum capacity of the room")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the room")

    def __str__(self):
        return self.name


class Reservation(models.Model):
    """
    The Reservation model represents a booking made by a user.
    It establishes foreign key relationships with both the Room and the User models.
    """
    STATUS_CHOICES = [
        'pending',
        'confirmed',
        'cancelled'
    ]
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reservations', on_delete=models.CASCADE)
    start_time = models.DateTimeField(help_text="Reservation start time")
    end_time = models.DateTimeField(help_text="Reservation end time")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Time the reservation was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Time the reservation was last updated")

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"Reservation for {self.room.name} by {self.user.username} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        """
        验证预订时间是否与现有预订冲突。
        """
        overlapping_reservations = Reservation.objects.filter(
            room=self.room,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)

        if overlapping_reservations.exists():
            raise ValidationError("This reservation conflicts with an existing reservation, try another time.")


class CustomUser(AbstractUser):
    """
    扩展的用户模型，添加 is_admin 字段以区分管理员和普通用户。
    """
    is_admin = models.BooleanField(default=False, help_text="Check if user is admin")

    def __str__(self):
        return self.username
