from core.settings import *


INSTALLED_APPS += ["django_extensions", "debug_toolbar"]

MIDDLEWARE.insert(3, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = [
    "127.0.0.1",
]
