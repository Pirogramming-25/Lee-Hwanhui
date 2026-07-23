from functools import wraps
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect


def model_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        query = urlencode(
            {
                "next": request.path,
                "required": "1",
            }
        )
        login_url = getattr(settings, "LOGIN_URL", "/accounts/login/")

        return redirect(f"{login_url}?{query}")

    return wrapper