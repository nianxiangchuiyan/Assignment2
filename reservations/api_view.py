from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from rest_framework import viewsets, permissions

from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer, UserSerializer

User = get_user_model()


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Reservation.objects.all()
        date_str = self.request.query_params.get('date')
        print("🔍 Filtering by date:", date_str)
        if date_str:
            print("✅ Matched reservations:", list(qs))
            try:
                start = make_aware(datetime.strptime(date_str, '%Y-%m-%d'))
                end = start + timedelta(days=1)
                qs = qs.filter(start_time__gte=start, start_time__lt=end)
            except Exception as e:
                print("Date parse error:", e)
        return qs

    def perform_create(self, serializer):
        print(f"calling perform_create")
        instance = serializer.save(user=self.request.user)
        instance.full_clean()
        instance.save()
        print(f"Reservation created: {instance}")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
