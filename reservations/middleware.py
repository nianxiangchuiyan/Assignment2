from django.utils import timezone
from .models import Reservation


class CleanPastReservationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 清理逻辑：删除已过期预约
        now = timezone.now()
        Reservation.objects.filter(end_time__lt=now).delete()

        # 正常继续处理请求
        response = self.get_response(request)
        return response
