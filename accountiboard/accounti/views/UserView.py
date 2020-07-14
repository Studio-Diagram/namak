import json
from datetime import datetime
from accounti.models import *
from django.contrib.auth.hashers import make_password
from accountiboard.constants import *
from accounti.validators.UserValidator import *
from accountiboard.custom_permissions import *


def register_user(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    validator = RegisterUserValidator(rec_data)
    if not validator.is_valid():
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    password_validator = PasswordValidator(min_digits=8)
    # password_validator.validate(rec_data.get('password'))
    password_validator.validate_with_re_password(rec_data.get('password'), rec_data.get('re_password'))
    if password_validator.get_errors():
        return JsonResponse({"response_code": 3, "error_msg": NOT_SIMILAR_PASSWORD})

    try:
        new_user = User(
            phone=rec_data.get('phone'),
            first_name=rec_data.get('first_name'),
            last_name=rec_data.get('last_name'),
            email=rec_data.get('email'),
            password=make_password(rec_data.get('password')),
            user_type=USER_TYPE['cafe_owner']
        )
        new_user.save()
        new_organization = Organization(
            name=rec_data.get('company_name'),
            shortcut_login_url=rec_data.get('company_name')
        )
        new_organization.save()
        CafeOwner(
            user=new_user,
            organization=new_organization
        ).save()
        Branch(
            name=BRANCH_DEFAULT_DATA.get('NAME'),
            start_working_time=datetime.strptime(BRANCH_DEFAULT_DATA.get('STARTING_TIME'), "%H:%M"),
            end_working_time=datetime.strptime(BRANCH_DEFAULT_DATA.get('ENDING_TIME'), "%H:%M"),
            min_paid_price=BRANCH_DEFAULT_DATA.get('MIN_PAID_PRICE'),
            game_data=[json.dumps(game_json) for game_json in BRANCH_DEFAULT_DATA.get('GAME_DATA')],
            organization=new_organization
        ).save()
    except Exception as e:
        print(e)
        return JsonResponse({"response_code": 3, "error_msg": ERROR_IN_CREATING})
    return JsonResponse({"response_code": 2})
