from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = [".pogonareport.com","localhost","web"]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True

with open('/src/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

try:
    from .local import *
except ImportError:
    pass
