import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Assignment1.settings")
app = get_asgi_application()
print("Django loaded from vercel_handler")
