from django.contrib.auth.hashers import make_password, check_password
from accounti.validators.UserValidator import *
from accountiboard.custom_permissions import *
from accountiboard.sms import *
from django.views import View
from django.shortcuts import get_object_or_404
from django.conf import settings


class PhoneVerifyView(View):
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        phone = rec_data.get('phone')
        verify_type = rec_data.get('verify_type')
        recaptcha_response_token = rec_data.get('recaptcha_response_token')

        if not phone or not recaptcha_response_token or not verify_type:
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        phone_validator = PhoneNumberValidator()
        phone_validator.validate(phone)
        if phone_validator.get_errors():
            return JsonResponse({"error_msg": phone_validator.get_errors()[0]}, status=400)

        if verify_type == "REGISTER":
            sms_template = settings.SMS_TEMPLATES.get('REGISTRATION')
            if User.objects.filter(phone=phone).count() > 0:
                return JsonResponse({"error_msg": PHONE_ALREADY_EXIST}, status=403)
        elif verify_type == "FORGET":
            sms_template = settings.SMS_TEMPLATES.get('FORGET_PASSWORD')
        else:
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        recaptcha_verify_data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response_token,
        }

        recaptcha_request = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_verify_data)
        recaptcha_request_json = recaptcha_request.json()

        if recaptcha_request_json['success']:
            send_verify_phone_sms(phone, sms_template)

        else:
            return JsonResponse({
                'error_msg': CAPTCHA_INVALID,
            }, status=401)

        return JsonResponse({
            'msg': f'sms sent to {phone}',
        }, status=200)


class RegisterCafeOwnerView(View):
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))

        validator = RegisterCafeOwnerValidator(rec_data)
        if not validator.is_valid():
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        phone = rec_data.get('phone')
        first_name = rec_data.get('first_name')
        last_name = rec_data.get('last_name')
        password = rec_data.get('password')
        re_password = rec_data.get('re_password')
        company_name = rec_data.get('company_name')
        company_address = rec_data.get('company_address')
        start_working_time = rec_data.get('start_working_time')
        end_working_time = rec_data.get('end_working_time')
        sms_verify_token = rec_data.get('sms_verify_token')
        sms_verified = False

        phone_validator = PhoneNumberValidator()
        phone_validator.validate(phone)
        if phone_validator.get_errors():
            return JsonResponse({"error_msg": phone_validator.get_errors()[0]}, status=400)

        password_validator = PasswordValidator(min_digits=8)
        password_validator.validate_with_re_password(password, re_password)
        if password_validator.get_errors():
            return JsonResponse({"error_msg": NOT_SIMILAR_PASSWORD}, status=400)

        sms_tokens = SmsToken.objects.filter(phone=phone)

        if sms_tokens.count() < 1:
            return JsonResponse({
                'error_msg': PHONE_VALIDATOR_ERROR,
            }, status=401)

        for sms_token in sms_tokens:
            if sms_token.token == sms_verify_token:
                sms_verified = True
                break

        if not sms_verified:
            return JsonResponse({'error_msg': PHONE_VALIDATOR_ERROR}, status=401)

        try:
            start_working_time = datetime.strptime(start_working_time, "%H:%M")
            end_working_time = datetime.strptime(end_working_time, "%H:%M")
        except:
            start_working_time = datetime.strptime("08:00", "%H:%M")
            end_working_time = datetime.strptime("23:00", "%H:%M")

        if User.objects.filter(phone=phone).count() > 0:
            return JsonResponse({"error_msg": PHONE_ALREADY_EXIST}, status=403)

        try:
            new_user = User(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password),
                user_type=USER_TYPE['cafe_owner'],
                is_active=True,
            )
            new_user.save()
            new_organization = Organization(
                name=company_name,
                shortcut_login_url=company_name,
            )
            new_organization.save()
            CafeOwner(
                user=new_user,
                organization=new_organization
            ).save()
            Branch(
                name=BRANCH_DEFAULT_DATA['NAME'],
                start_working_time=start_working_time,
                end_working_time=end_working_time,
                min_paid_price=BRANCH_DEFAULT_DATA['MIN_PAID_PRICE'],
                game_data=[json.dumps(game_json) for game_json in BRANCH_DEFAULT_DATA.get('GAME_DATA')],
                address=company_address,
                organization=new_organization
            ).save()
        except Exception as e:
            return JsonResponse({"error_msg": ERROR_IN_CREATING}, status=403)

        sms_tokens.delete()
        return JsonResponse({"msg": "CafeOwner user created successfully."})


class ForgotPasswordView(View):
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        sms_verified = False

        validator = ForgotPasswordValidator(rec_data)
        if not validator.is_valid():
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        phone = rec_data['phone']
        password = rec_data['password']
        re_password = rec_data['re_password']
        sms_verify_token = rec_data['sms_verify_token']

        if User.objects.filter(phone=phone).count() < 1:
            return JsonResponse({"error_msg": PHONE_DOESNT_EXIST}, status=403)

        password_validator = PasswordValidator(min_digits=8)
        password_validator.validate_with_re_password(password, re_password)
        if password_validator.get_errors():
            return JsonResponse({"error_msg": NOT_SIMILAR_PASSWORD}, status=403)

        sms_tokens_count = SmsToken.objects.filter(phone=phone).count()
        sms_tokens = SmsToken.objects.filter(phone=phone)

        if sms_tokens_count < 1:
            return JsonResponse({
                'error_msg': 'You have to validate your phone number first',
            }, status=401)

        for sms_token in sms_tokens:
            if sms_token.token == sms_verify_token:
                sms_verified = True
                break

        if not sms_verified:
            return JsonResponse({'error_msg': PHONE_VALIDATOR_ERROR}, status=401)

        current_user = User.objects.get(phone=phone)
        current_user.password = make_password(password)
        current_user.save()

        sms_tokens.delete()
        return JsonResponse({"msg": "Password was changed successfully"})


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


class ProfileView(View):
    @jwt_decoder_decorator_class_based()
    def get(self, request, *args, **kwargs):
        user_object = get_object_or_404(User, pk=request.jwt_payload.get('sub_id'))
        return JsonResponse({
            "_item": {
                "id": user_object.pk,
                "first_name": user_object.first_name,
                "last_name": user_object.last_name,
                "phone": user_object.phone,
                "email": user_object.email,
                "home_address": user_object.home_address
            }
        })

    @jwt_decoder_decorator_class_based()
    def put(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        validator = ProfileValidator(rec_data)
        if not validator.is_valid():
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        user_object = get_object_or_404(User, pk=request.jwt_payload.get('sub_id'))
        user_object.first_name = rec_data.get('first_name')
        user_object.last_name = rec_data.get('last_name')
        user_object.phone = rec_data.get('phone')
        user_object.email = rec_data.get('email')
        user_object.home_address = rec_data.get('home_address')

        user_object.save()
        return JsonResponse({})


class ChangePasswordView(View):
    @jwt_decoder_decorator_class_based()
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        validator = ChangePasswordValidator(rec_data)
        if not validator.is_valid():
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        old_password = rec_data.get('old_password')
        new_password = rec_data.get('new_password')
        re_new_password = rec_data.get('re_new_password')

        password_validator = PasswordValidator(min_digits=8)
        password_validator.validate_with_re_password(new_password, re_new_password)

        user_object = get_object_or_404(User, pk=request.jwt_payload.get('sub_id'))

        if password_validator.get_errors() or not check_password(old_password, user_object.password):
            return JsonResponse({"error_msg": NOT_SIMILAR_PASSWORD_OR_WRONG_PASSWORD}, status=400)

        user_object.password = make_password(new_password)

        user_object.save()
        return JsonResponse({'msg': PASSWORD_CHANGED})
