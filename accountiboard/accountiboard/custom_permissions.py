from accountiboard.constants import UNAUTHENTICATED, ACCESS_DENIED, NO_MESSAGE
from accountiboard.utils import decode_JWT_return_user
from functools import wraps
from django.http import JsonResponse
import json


def permission_decorator(permission_func, permitted_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            permission_result = permission_func(request, permitted_roles, *args, **kwargs)
            if permission_result[0]:
                return view_func(request, *args, **kwargs)
            return JsonResponse({"response_code": 3, "error_msg": permission_result[1]})

        return _wrapped_view

    return decorator


def session_authenticate(request, permitted_roles):
    user_roles = request.session.get('user_role', None)
    if request.session.get('is_logged_in', None) or user_roles:
        for role in user_roles:
            if role in permitted_roles:
                return True, NO_MESSAGE
        return False, ACCESS_DENIED
    return False, UNAUTHENTICATED


def token_authenticate(request, permitted_roles):
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    request_branch = get_branch(request)
    if not payload:
        return False, UNAUTHENTICATED

    for role in payload['sub_roles']:
        if role in permitted_roles:
            if request_branch in payload['sub_branch_list']:
                return True, NO_MESSAGE
    return False, ACCESS_DENIED

def get_branch(request):
    body_unicode = request.body.decode('utf-8')
    rec_data = json.loads(body_unicode)
    branch = None
    if 'branch' in rec_data:
        branch = rec_data['branch']
    elif 'branch_id' in rec_data:
        branch = rec_data['branch_id']
    # elif 'pk' in request.kwargs:
    #     branch = request.kwargs['pk']

    return branch

