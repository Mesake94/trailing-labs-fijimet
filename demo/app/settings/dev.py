from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-l$ny4bjb0il6n(f8w(^%z4)mh!n1m(2#&0kty7bs(=zbfx(d)k"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
