from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from accountiboard.utils import *
from django.views import View
from django.shortcuts import get_object_or_404, redirect
import jdatetime
from django.db.models import Sum
from django.conf import settings
from datetime import datetime, timedelta
import requests
import re
import jdatetime

RE_DURATION = re.compile(r"[\d]+", flags=re.ASCII)

def calculate_discount(amount, discount, bundle, cafe_owner):
    if datetime.now() > discount.expire_time:
        return (amount, False, 'Discount time expired')

    if discount.num_of_use != None and discount.num_of_use < 1:
        return (amount, False, 'Discount has no more uses left')

    if discount.cafe_owner != None and discount.cafe_owner != cafe_owner:
        return (amount, False, 'This discount code is defined for another cafe owner')

    if discount.bundle:
        discount_bundle_splitted = discount.bundle.split('_')
        if len(discount_bundle_splitted) == 1 and discount.bundle != bundle.split('_')[0]:
            return (amount, False, 'This discount code is defined for another bundle type')
        elif len(discount_bundle_splitted) == 2 and discount.bundle != bundle:
            return (amount, False, 'This discount code is defined for another bundle type')

    if discount.type == 'amount':
        amount = AVAILABLE_BUNDLES[bundle] - discount.quantity
    elif discount.type == 'percent':
        discount_amount = (discount.quantity / 100) * AVAILABLE_BUNDLES[bundle]
        if discount.max_discount_amount and not discount.min_discount_amount and discount_amount > discount.max_discount_amount:
            discount_amount = discount.max_discount_amount
        elif discount.min_discount_amount and not discount.max_discount_amount and discount_amount < discount.min_discount_amount:
            discount_amount = discount.min_discount_amount
        elif discount.max_discount_amount and discount.min_discount_amount:
            if discount_amount < discount.min_discount_amount:
                discount_amount = discount.min_discount_amount
            elif discount_amount > discount.max_discount_amount:
                discount_amount = discount.max_discount_amount

        amount = AVAILABLE_BUNDLES[bundle] - discount_amount

    return (amount, True, f'Discount code "{discount.name}" applied.')

class BundleView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def get(self, request, *args, **kwargs):
        payload = request.payload

        current_cafe_owner = CafeOwner.objects.get(pk=payload['sub_id'])

        active_bundle = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_active=True)
        reserved_bundles = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_reserved=True)
        expired_bundles = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_expired=True)
        not_successfully_paid_bundles = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_active=False, is_expired=False, is_reserved=False)

        return JsonResponse({
                    'active_bundle': [{
                    "bundle_plan": bundle.bundle_plan,
                    "bundle_duration": bundle.bundle_duration,
                    "starting_datetime_plan": jdatetime.datetime.fromgregorian(datetime=bundle.starting_datetime_plan).strftime("%H:%M %Y/%m/%d") if
                        bundle.starting_datetime_plan else '',
                    "expiry_datetime_plan": jdatetime.datetime.fromgregorian(datetime=bundle.expiry_datetime_plan).strftime("%H:%M %Y/%m/%d") if
                        bundle.expiry_datetime_plan else '',
                    "is_active": bundle.is_active,
                    "is_reserved": bundle.is_reserved,
                    "is_expired": bundle.is_expired,
                    } for bundle in active_bundle],

                    'reserved_bundles': [{
                    "bundle_plan": bundle.bundle_plan,
                    "bundle_duration": bundle.bundle_duration,
                    "starting_datetime_plan": jdatetime.datetime.fromgregorian(datetime=bundle.starting_datetime_plan).strftime("%H:%M %Y/%m/%d") if
                        bundle.starting_datetime_plan else '',
                    "expiry_datetime_plan": jdatetime.datetime.fromgregorian(datetime=bundle.expiry_datetime_plan).strftime("%H:%M %Y/%m/%d") if
                        bundle.expiry_datetime_plan else '',
                    "is_active": bundle.is_active,
                    "is_reserved": bundle.is_reserved,
                    "is_expired": bundle.is_expired,
                    } for bundle in reserved_bundles],

                    'expired_bundles': [{
                    "bundle_plan": bundle.bundle_plan,
                    "bundle_duration": bundle.bundle_duration,
                    "starting_datetime_plan": jdatetime.datetime.fromgregorian(datetime=bundle.starting_datetime_plan).strftime("%H:%M %Y/%m/%d") if
                        bundle.starting_datetime_plan else '',
                    "expiry_datetime_plan": jdatetime.datetime.fromgregorian(datetime=bundle.expiry_datetime_plan).strftime("%H:%M %Y/%m/%d") if
                        bundle.expiry_datetime_plan else '',
                    "is_active": bundle.is_active,
                    "is_reserved": bundle.is_reserved,
                    "is_expired": bundle.is_expired,
                    } for bundle in expired_bundles],

                    'not_successfully_paid_bundles': [{
                    "bundle_plan": bundle.bundle_plan,
                    "bundle_duration": bundle.bundle_duration,
                    "starting_datetime_plan": jdatetime.datetime.fromgregorian(datetime=bundle.starting_datetime_plan).strftime("%H:%M %Y/%m/%d") if
                        bundle.starting_datetime_plan else '',
                    "expiry_datetime_plan": jdatetime.datetime.fromgregorian(datetime=bundle.expiry_datetime_plan).strftime("%H:%M %Y/%m/%d") if
                        bundle.expiry_datetime_plan else '',
                    "is_active": bundle.is_active,
                    "is_reserved": bundle.is_reserved,
                    "is_expired": bundle.is_expired,
                    } for bundle in not_successfully_paid_bundles],

        }, status=200)

    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        bundle = rec_data.get('bundle')
        discount_code = rec_data.get('discount_code')
        payload = request.payload
        current_discount_obj = None

        if bundle not in AVAILABLE_BUNDLES:
            return JsonResponse({
                'error_msg': BUNDLE_NOT_AVAILABLE
            }, status=400)

        if discount_code:
            try:
                current_discount_obj = SubscriptionDiscount.objects.get(code=discount_code)
            except:
                return JsonResponse({
                    'error_msg': SUBSCRIPTION_DISCOUNT_NOT_AVAILABLE
                }, status=400)

        current_user = User.objects.get(pk=payload['sub_id'])
        current_cafe_owner = CafeOwner.objects.get(user=current_user)
        active_bundle_count = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_active=True).count()
        reserved_bundle_count = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_reserved=True).count()

        days = RE_DURATION.findall(bundle)[0]
        bundle_type = bundle.replace(f"_{days}", "")
        amount = AVAILABLE_BUNDLES[bundle]

        if active_bundle_count > 0 and reserved_bundle_count > 0:
            return JsonResponse({
                'error_msg': ALREADY_HAVE_ACTIVE_AND_RESERVE_BUNDLE
            }, status=403)

        if active_bundle_count > 0:
            new_bundle_is_reserved = True
            current_active_bundle = Bundle.objects.get(cafe_owner=current_cafe_owner, is_active=True)
            if BUNDLE_WEIGHTS[bundle_type] < BUNDLE_WEIGHTS[current_active_bundle.bundle_plan]:
                return JsonResponse({
                    'error_msg': DOWNGRADING_BUNDLES_NOT_POSSIBLE
                }, status=403)
            bundle_start_time = current_active_bundle.expiry_datetime_plan
        else:
            new_bundle_is_reserved = False
            bundle_start_time = datetime.utcnow()

        discount_applied = False
        discount_msg = 'No discount code was applied.'

        if discount_code:
            discount_result = calculate_discount(amount, current_discount_obj, bundle, current_cafe_owner)
            if discount_result[1]:
                discount_applied = True
            discount_msg = discount_result[2]
            amount = discount_result[0]

            if not discount_applied:
                return JsonResponse({
                            'msg': "Discount code not valid",
                            'bundle': bundle,
                            'discount_applied': discount_applied,
                            'discount_msg': discount_msg,
                }, status=403)

        current_transaction = Transaction.objects.create(
            subscription_discount=current_discount_obj,
            cafe_owner = current_cafe_owner,
            status = "Not paid yet",
            token = "No token yet",
            amount = amount,
            mobile = payload['sub_phone'],
            redirect = settings.PAY_IR_REDIRECT_URL,
            card_number = "Not paid yet",
            trans_id = "Not paid yet",
        )

        current_bundle = Bundle.objects.create(
            bundle_plan = bundle_type,
            bundle_duration = days,
            starting_datetime_plan = bundle_start_time,
            expiry_datetime_plan = bundle_start_time + timedelta(days=int(days), seconds=5),
            is_active = False,
            is_reserved = new_bundle_is_reserved,
            cafe_owner = current_cafe_owner,
            transaction = current_transaction,
        )

        init_data = {
            "api": settings.PAY_IR_API_KEY,
            "amount" : amount,
            "redirect": settings.PAY_IR_REDIRECT_URL,
            "factorNumber" : current_transaction.factor_number,
            "mobile" : payload['sub_phone'],
            'description' : None,
        }
        try:
            response = get_json(requests.post(settings.PAY_IR_API_URL_SEND, data=init_data))
            if response['status'] != 1:
                return JsonResponse({
                    'error_msg': "Could not init transaction (status error)"
                }, status=400)
        except Exception as e:
            raise e

        current_transaction.token = response["token"]
        current_transaction.save()

        return JsonResponse({
                    'msg': "Please pay your transaction",
                    'bundle': bundle,
                    'discount_applied': discount_applied,
                    'discount_msg': discount_msg,
                    'final_price': amount,
                    'redirect' : settings.PAY_IR_API_URL_PAYMENT_GATEWAY.format(token=response["token"])
        }, status=200)


class PayirVerifyGenNewTokenView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        status = rec_data.get('status')
        token = rec_data.get('token')

        if status == "1":

            verify_data = {
                "api" : settings.PAY_IR_API_KEY,
                "token": token,
            }

            try:
                response = get_json(requests.post(settings.PAY_IR_API_URL_VERIFY, data=verify_data))
                if response['status'] != 1:
                    return JsonResponse({
                        'error_msg': "Could not verify transaction (status error)"
                    }, status=400)
            except Exception as e:
                raise e

            current_transaction = Transaction.objects.get(token=token)

            if current_transaction.status == "paid":
                return JsonResponse({
                    'error_msg': "Transaction already verified"
                }, status=400)

            current_transaction.trans_id = response["transId"]
            current_transaction.card_number = response["cardNumber"]
            current_transaction.status = "paid"

            if current_transaction.subscription_discount and current_transaction.subscription_discount.num_of_use:
                current_transaction.subscription_discount.num_of_use -= 1
                current_transaction.subscription_discount.save()

            current_transaction.save()

            current_bundle = Bundle.objects.get(transaction=current_transaction)

            current_cafe_owner = current_bundle.cafe_owner

            old_active_bundles_count = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_active=True).count()

            if old_active_bundles_count > 0:
                current_bundle.is_reserved = True
            else:
                current_bundle.is_active = True

            current_bundle.save()

            # adding cafe owner and all related employees to TokenBlacklist
            if current_bundle.is_active:
                TokenBlacklist.objects.create(user=current_cafe_owner.user)
                all_branches = Branch.objects.filter(organization=current_cafe_owner.organization)
                for branch in all_branches:
                    all_employees = EmployeeToBranch.objects.filter(branch=branch)
                    for employee in all_employees:
                        TokenBlacklist.objects.create(user=employee.employee.user)

                bundle_activation_status = "activated"
            elif current_bundle.is_reserved:
                bundle_activation_status = "reserved"

        else:
            return JsonResponse({
                'error_msg': "unsuccessful transaction (status not 1 pre)",
                'bundle_activation_status' : "unsuccessful"
            }, status=400)


        try:
            user_obj = User.objects.get(phone=request.payload['sub_phone'])
        except ObjectDoesNotExist:
            return JsonResponse({"error_msg": WRONG_USERNAME_OR_PASS}, status=401)

        cafe_owner_object = CafeOwner.objects.get(user=user_obj)
        organization_object = cafe_owner_object.organization
        organization_name = organization_object.name
        branch_object = Branch.objects.filter(organization=organization_object).first().id
        user_branch_objects = Branch.objects.filter(organization=organization_object)
        user_branches = [{
            "id": cafe_owner_to_branch.id,
            "name": cafe_owner_to_branch.name
        } for cafe_owner_to_branch in user_branch_objects]
        user_role = [USER_ROLES['CAFE_OWNER']]
        try:
            bundle = Bundle.objects.get(cafe_owner=cafe_owner_object, is_active=True).bundle_plan
        except:
            bundle = USER_PLANS_CHOICES['FREE']
        jwt_token = make_new_JWT_token(
            user_obj.id,
            user_obj.phone,
            user_role,
            bundle,
            user_branches,
            organization_object.id,
        )
        return JsonResponse(
            {"response_code": 2,
             "user_data": {'branch': branch_object, 'full_name': user_obj.get_full_name(),
                           'branches': user_branches,
                           'user_roles': user_role,
                           'bundle': bundle,
                           'organization_name': organization_name
                           },
             "bundle_activation_status" : bundle_activation_status,
             "token": jwt_token.decode("utf-8")
             }
        )



class CheckSubscriptionDiscountView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        code = rec_data.get('discount_code')
        bundle = rec_data.get('bundle')
        amount = AVAILABLE_BUNDLES[bundle]

        payload = request.payload
        current_cafe_owner = CafeOwner.objects.get(pk=payload['sub_id'])

        discount_applied = False
        discount_msg = 'No discount code was applied.'

        try:
            current_discount_obj = SubscriptionDiscount.objects.get(code=code)
        except:
            return JsonResponse({
                'msg': "subscription discount code does not exist."
            }, status=403)


        discount_result = calculate_discount(amount, current_discount_obj, bundle, current_cafe_owner)
        if discount_result[1]:
            discount_applied = True
        discount_msg = discount_result[2]
        amount_after_discount = discount_result[0]

        if not discount_applied:
            return JsonResponse({
                        'msg': "Discount code not valid",
                        'bundle': bundle,
                        'discount_applied': discount_applied,
                        'discount_msg': discount_msg,
            }, status=403)
        else:
            return JsonResponse({
                        'msg': "Discount code is valid",
                        'bundle': bundle,
                        'discount_applied': discount_applied,
                        'discount_msg': discount_msg,
                        'amount': amount - amount_after_discount
            }, status=200)


class TransactionsView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def get(self, request, *args, **kwargs):
        payload = request.payload

        current_cafe_owner = CafeOwner.objects.get(pk=payload['sub_id'])

        all_transactions = Transaction.objects.filter(cafe_owner=current_cafe_owner)

        return JsonResponse({
                    'all_transactions': [{
                    "status": transaction.status,
                    "token": transaction.token,
                    "amount": transaction.amount,
                    "mobile": transaction.mobile,
                    "factor_number": transaction.factor_number,
                    "description": transaction.description,
                    "redirect": transaction.redirect,
                    "card_number": transaction.card_number,
                    "trans_id": transaction.trans_id,
                    "message": transaction.message,
                    } for transaction in all_transactions]

        }, status=200)
