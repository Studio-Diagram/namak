from accountiboard.constants import UNAUTHENTICATED, ACCESS_DENIED, NO_MESSAGE, BRANCH_NOT_IN_SESSION_ERROR
from accountiboard.utils import decode_JWT_return_user
from functools import wraps
from django.http import JsonResponse
import json
import jwt
from accountiboard.settings import JWT_SECRET
# from accountiboard.utils import *
import datetime
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


def session_authenticate(request, permitted_roles, branch_disable=False):
    user_roles = request.session.get('user_role', None)
    if request.session.get('is_logged_in', None) and user_roles:
        request_branch = get_branch(request)
        session_branch = request.session.get('branch_list', None)
        if not session_branch:
            return {
                "state": False,
                "message": BRANCH_NOT_IN_SESSION_ERROR
            }
        for role in user_roles:
            if role in permitted_roles:
                if branch_disable or request_branch in session_branch:
                    return {
                        "state": True,
                        "message": NO_MESSAGE
                    }
        return {
            "state": False,
            "message": ACCESS_DENIED
        }
    return {
        "state": False,
        "message": UNAUTHENTICATED
    }



def token_authenticate(request, permitted_roles, bundles, branch_disable=False, *args, **kwargs):
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    request_branch = get_branch(request)
    if not payload:
        return {
            "state": False,
            "message": UNAUTHENTICATED
        }

    if TokenBlacklist.objects.filter(user=payload['sub_id']).count() > 0:
        for blacklist_obj in TokenBlacklist.objects.filter(user=payload['sub_id']):
            if datetime.datetime.utcfromtimestamp(payload['iat']) < blacklist_obj.created_time:
                return {
                    "state": False,
                    "message": UNAUTHENTICATED
                }

    # Adding 'FREE' plan to bundle definition on view decorators and also JWT token:
    bundles.add('FREE')
    payload_bundles = {payload['sub_bundle'], 'FREE'}

    for role in payload['sub_roles']:
        if role in permitted_roles:
            if bundles.issubset(payload_bundles):
                if branch_disable or any(branch.get('id') == request_branch for branch in payload['sub_branch_list']):
                    return {
                        "state": True,
                        "message": NO_MESSAGE,
                        "payload": payload
                    }
    return {
        "state": False,
        "message": ACCESS_DENIED
    }


def get_branch(request):
    try:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            rec_data = json.loads(body_unicode)
            branch = None
            if 'branch' in rec_data:
                branch = rec_data['branch']
            elif 'branch_id' in rec_data:
                branch = rec_data['branch_id']
            return branch
        elif request.method == 'GET':
            branch_str = request.GET.get('branch', None)
            if branch_str:
                branch = int(branch_str)
            return branch
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
