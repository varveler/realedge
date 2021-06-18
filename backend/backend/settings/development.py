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


INSTALLED_APPS += [
    "django_extensions",
]

SHELL_PLUS = "ipython"

#SHELL_PLUS_PRINT_SQL = True

NOTEBOOK_ARGUMENTS = [
    "--ip",
    "0.0.0.0",
    "--port",
    "8888",
    "--allow-root",
    "--no-browser",
]

IPYTHON_ARGUMENTS = [
    "--ext",
    "django_extensions.management.notebook_extension",
    "--debug",
]

IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"

# SHELL_PLUS_POST_IMPORTS = [ # extra things to import in notebook
#     ("module1.submodule", ("func1", "func2", "class1", "etc")),
#     ("module2.submodule", ("func1", "func2", "class1", "etc"))
#
# ]

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true" # only use in development


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
]
