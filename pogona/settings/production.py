from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = [".pogona.org","localhost","web"]

with open('/src/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

try:
    from .local import *
except ImportError:
    pass
