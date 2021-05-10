from .base import *
#from corsheaders.defaults import default_headers

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

#print "running on settings base and development"

#OAUTH2_REDIRECT_URI = 'http://localhost/oauth2/oauth2callback'

#CORS_URLS_REGEX = r'^/radar.*'
#CORS_ORIGIN_ALLOW_ALL = True
#CORS_ORIGIN_WHITELIST = (
    #'*',
    #'http://localhost:3000',
    #'your-bucket-here.s3-us-west-2.amazonaws.com',
#)

# CORS_ALLOW_HEADERS = default_headers + (
#     'Access-Control-Allow-Origin',
# )
