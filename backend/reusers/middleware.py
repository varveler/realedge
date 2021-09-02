from rest_framework.request import Request
from django.contrib.auth.middleware import get_user
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

class AuthenticationMiddlewareJWT(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.get_full_path_info() not in ['/token/', '/token/refresh/']:
            print(request.user)
            try:
                user_jwt = JWTAuthentication().authenticate(Request(request))
            except Exception as e:
                print('error was', e)
                return JsonResponse(status=401, data={'code': 'token_not_valid'})
            user = get_user(request)
            if user.is_authenticated:
                request.user = user
            elif user_jwt is not None:
                request.user = user_jwt[0]
