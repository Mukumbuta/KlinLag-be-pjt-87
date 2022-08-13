from .models import User
from django.core.exceptions import PermissionDenied


def user_is_giver(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        if user.is_giver:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_collector(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        if user.is_collector:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
