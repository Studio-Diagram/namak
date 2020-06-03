from accountiboard.constants import UNAUTHENTICATED
from accountiboard.utils import decode_JWT_return_user
from functools import wraps
from django.http import JsonResponse

def permission_decorator(permission_func, min_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if permission_func(request, min_role, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            return JsonResponse({"response_code": 401, "error_msg": UNAUTHENTICATED})
        return _wrapped_view
    return decorator


def session_authenticate(request, min_role):
    if request.session['is_logged_in'] and request.session['user_role']:
        return True
    return False


def token_authenticate(request, min_role):
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    if not payload:
        return False
    if min_role in payload['sub_roles']:
        return True
    return False