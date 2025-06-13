from django.apps import AppConfig


class LessonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reservations"


class FixturesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    path = "reservations/fixtures/initial_rooms.json"
