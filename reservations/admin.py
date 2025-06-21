# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Room, Reservation, CustomUser


# 5.1 Room 管理
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'capacity']
    search_fields = ['name', 'location']


# 5.2 + 5.3 + 5.4 Reservation 管理
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'start_time', 'end_time']
    list_filter = ['room', 'start_time']
    search_fields = ['user__username', 'room__name']
    autocomplete_fields = ['room', 'user']
    date_hierarchy = 'start_time'


# 5.5 User 管理
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_admin', 'is_staff', 'is_superuser']
    list_filter = ['is_admin', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
