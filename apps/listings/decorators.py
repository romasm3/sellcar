# apps/listings/decorators.py
from functools import wraps
from django.http import Http404


def staff_only(view_func):
    """WIP kategorijos pasiekiamos TIK staff'ui. Visi kiti gauna 404."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return view_func(request, *args, **kwargs)
    return wrapper