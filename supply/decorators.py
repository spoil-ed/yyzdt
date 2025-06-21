from django.http import HttpResponseForbidden
from django.shortcuts import render
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return render(request, 'login.html')
            if hasattr(request.user, 'role') and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return render(request, '403.html')
        return wrapper
    return decorator