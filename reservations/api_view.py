from django.contrib.auth import get_user_model
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
        # date = self.request.query_params.get('date')
        # if date:
        #     # 过滤 start_time 的日期部分
        #     qs = qs.filter(start_time__date=date)
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
