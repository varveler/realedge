from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['api.realedge.io']

CORS_ALLOWED_ORIGINS = [
    "http://realedge.io",
]

CORS_ALLOW_HEADERS = ['*']


#ALLOWED_HOSTS=['*']

CORS_ORIGIN_ALLOW_ALL = True
