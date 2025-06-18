# from django.contrib.auth import logout
# from django.contrib.auth.views import LogoutView
# from django.urls import path
# from . import views
# from .views import ProfileDetail
#
# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('', views.home, name='home'),
#
#     path('logout/', views.logout_view, name='logout'),
#     path('accounts/profile/', ProfileDetail.as_view(), name='profile_detail'),
#     path('', views.home, name='home'),
#     path('rooms/', views.room_list, name='room_list'),
#     path('rooms/<int:room_id>/reserve/', views.make_reservation, name='make_reservation'),
#     path('allrooms/', views.all_rooms_view, name='all_rooms'),
#
# ]

# reservations/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .api_view import RoomViewSet, ReservationViewSet, UserViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'users', UserViewSet)

# urlpatterns = router.urls
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
