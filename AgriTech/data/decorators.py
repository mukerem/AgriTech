from django.core.exceptions import PermissionDenied
from data.models import User, Role

from django.utils import timezone
from django.shortcuts import redirect


def federal_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role.short_name == 'federal':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def region_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role.short_name == 'region':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def zone_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role.short_name == 'zone':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def wereda_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role.short_name == 'wereda':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def advisor_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role.short_name == 'advisor':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

