# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


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


from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    room = models.ForeignKey(
        'Room',
        related_name='reservations',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='reservations',
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField(help_text="Reservation start time")
    end_time = models.DateTimeField(help_text="Reservation end time")

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['room', 'start_time', 'end_time']),
        ]

    def __str__(self):
        return f"{self.room.name} | {self.user.username} | {self.start_time:%Y-%m-%d %H:%M}"

    def clean(self):
        # 结束时间必须晚于开始时间
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

        # 冲突校验
        overlap = Reservation.objects.filter(
            room=self.room,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)

        if overlap.exists():
            raise ValidationError("This reservation conflicts with an existing reservation.")


class CustomUser(AbstractUser):
    """
    扩展的用户模型，添加 is_admin 字段以区分管理员和普通用户。
    """
    is_admin = models.BooleanField(default=False, help_text="Check if user is admin")

    def __str__(self):
        return self.username
