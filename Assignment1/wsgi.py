"""
WSGI config for Assignment1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from whitenoise import WhiteNoise

from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Assignment1.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), 'static'))
app = get_asgi_application()
