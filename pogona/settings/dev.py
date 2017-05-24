from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#)a*n=8t!(aq=h=l==i(&piw66vku=0vjy&bskgd^d67fl#)%e'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ["*"]


try:
    from .local import *
except ImportError:
    pass
