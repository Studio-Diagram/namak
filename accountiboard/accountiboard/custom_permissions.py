from accountiboard.constants import UNAUTHENTICATED, ACCESS_DENIED, NO_MESSAGE, ALL_PLANS_SET
from accountiboard.utils import decode_JWT_return_user
from functools import wraps
from django.http import JsonResponse, HttpResponseRedirect
import json
import jwt
from accountiboard.settings import JWT_SECRET
from datetime import datetime, timedelta
from accounti.models import TokenBlacklist


def permission_decorator(permission_func, permitted_roles, bundles, branch_disable=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            permission_result = permission_func(request, permitted_roles, bundles, branch_disable, *args, **kwargs)
            if permission_result.get('state'):
                if permission_result.get('payload'):
                    request.payload = permission_result.get('payload')
                return view_func(request, *args, **kwargs)
            return JsonResponse({"response_code": 3, "error_msg": permission_result.get('message')}, status=403)

        return _wrapped_view

    return decorator


def permission_decorator_class_based(permission_func, permitted_roles, bundles, branch_disable=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            permission_result = permission_func(request, permitted_roles, bundles, branch_disable, *args, **kwargs)
            if permission_result.get('state'):
                if permission_result.get('payload'):
                    request.payload = permission_result.get('payload')
                return view_func(self, request, *args, **kwargs)
            return JsonResponse({"response_code": 3, "error_msg": permission_result.get('message')}, status=403)

        return _wrapped_view

    return decorator

def permission_decorator_class_based_simplified(permission_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            permission_result = permission_func(request, *args, **kwargs)
            if permission_result.get('state'):
                return view_func(self, request, *args, **kwargs)
            return HttpResponseRedirect('/onward/login/')

        return _wrapped_view

    return decorator


def session_authenticate_admin_panel(request, *args, **kwargs):
    if request.session.get('admin_is_logged_in'):
        return {
            "state": True,
            "message": NO_MESSAGE
        }
    else:
        return {
            "state": False,
            "message": UNAUTHENTICATED
        }



def token_authenticate(request, permitted_roles, bundles, branch_disable=False, *args, **kwargs):
    view_bundles = ALL_PLANS_SET - bundles
    try:
        payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    except:
        return {
            "state": False,
            "message": UNAUTHENTICATED
        }
    if not payload:
        return {
            "state": False,
            "message": UNAUTHENTICATED
        }

    request_branch = get_branch(request, *args, **kwargs)
    token_black_list_objects = TokenBlacklist.objects.filter(user=payload['sub_id'])
    if token_black_list_objects.count() > 0:
        for blacklist_obj in token_black_list_objects:
            if datetime.fromtimestamp(payload['iat']) + timedelta(seconds=30) < blacklist_obj.created_time:
                return {
                    "state": False,
                    "message": UNAUTHENTICATED
                }

    for role in payload['sub_roles']:
        if role in permitted_roles:
            if payload['sub_bundle'] in view_bundles:
                if branch_disable or any(branch['id'] == request_branch for branch in payload['sub_branch_list']):
                    return {
                        "state": True,
                        "message": NO_MESSAGE,
                        "payload": payload
                    }
    return {
        "state": False,
        "message": ACCESS_DENIED
    }


def get_branch(request, *args, **kwargs):
    branch_list = []
    try:
        if request.method in {'POST', 'PUT'}:
            body_unicode = request.body.decode('utf-8')
            rec_data = json.loads(body_unicode)
            branch_list.extend([rec_data.get('branch_id'), rec_data.get('branch')])

        branch_list.extend([
            kwargs.get('branch_id'), kwargs.get('branch'),
            request.GET.get('branch_id'), request.GET.get('branch'),
        ])

        for branch in branch_list:
            if branch:
                return int(branch)
    except:
        return None


# This function is not needed:
# permission_decorator & permission_decorator_class_based already set request.payload
def jwt_decoder_decorator_class_based():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION').replace('Bearer ', '').strip()
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                request.jwt_payload = payload
                return view_func(self, request, *args, **kwargs)
            except Exception as e:
                return JsonResponse({"response_code": 3, "error_msg": "Invalid Token!"}, status=401)

        return _wrapped_view

    return decorator
