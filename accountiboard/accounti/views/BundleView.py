from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from accountiboard.utils import *
from django.views import View
from django.shortcuts import get_object_or_404
import jdatetime
from django.db.models import Sum
from django.conf import settings
from datetime import datetime, timedelta
import requests
import re

RE_DURATION = re.compile(r"[\d]+", flags=re.ASCII)

def calculate_discount(amount, discount, bundle, cafe_owner):
    if datetime.now() > discount.expire_time:
        return (amount, False, 'Discount time expired')

    if discount.num_of_use and discount.num_of_use < 1:
        return (amount, False, 'Discount has no more uses left')

    if discount.cafe_owner and discount.cafe_owner != cafe_owner:
        return (amount, False, 'This discount code is defined for another cafe owner')

    if discount.bundle and discount.bundle != bundle:
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
    @permission_decorator_class_based(
        token_authenticate,
        {USER_ROLES['CAFE_OWNER']},
        {USER_PLANS_CHOICES['FREE']},
        branch_disable=True
    )
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
                    "starting_datetime_plan": bundle.starting_datetime_plan,
                    "expiry_datetime_plan": bundle.expiry_datetime_plan,
                    "is_active": bundle.is_active,
                    "is_reserved": bundle.is_reserved,
                    "is_expired": bundle.is_expired,
                    } for bundle in active_bundle],

                    'reserved_bundles': [{
                    "bundle_plan": bundle.bundle_plan,
                    "bundle_duration": bundle.bundle_duration,
                    "starting_datetime_plan": bundle.starting_datetime_plan,
                    "expiry_datetime_plan": bundle.expiry_datetime_plan,
                    "is_active": bundle.is_active,
                    "is_reserved": bundle.is_reserved,
                    "is_expired": bundle.is_expired,
                    } for bundle in reserved_bundles],

                    'expired_bundles': [{
                    "bundle_plan": bundle.bundle_plan,
                    "bundle_duration": bundle.bundle_duration,
                    "starting_datetime_plan": bundle.starting_datetime_plan,
                    "expiry_datetime_plan": bundle.expiry_datetime_plan,
                    "is_active": bundle.is_active,
                    "is_reserved": bundle.is_reserved,
                    "is_expired": bundle.is_expired,
                    } for bundle in expired_bundles],

                    'not_successfully_paid_bundles': [{
                    "bundle_plan": bundle.bundle_plan,
                    "bundle_duration": bundle.bundle_duration,
                    "starting_datetime_plan": bundle.starting_datetime_plan,
                    "expiry_datetime_plan": bundle.expiry_datetime_plan,
                    "is_active": bundle.is_active,
                    "is_reserved": bundle.is_reserved,
                    "is_expired": bundle.is_expired,
                    } for bundle in not_successfully_paid_bundles],

        }, status=200)

    @permission_decorator_class_based(
        token_authenticate,
        {USER_ROLES['CAFE_OWNER']},
        {USER_PLANS_CHOICES['FREE']},
        branch_disable=True
    )
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

        current_cafe_owner = CafeOwner.objects.get(pk=payload['sub_id'])
        active_bundle_count = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_active=True).count()
        reserved_bundle_count = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_reserved=True).count()

        days = RE_DURATION.findall(bundle)[0]
        bundle_type = bundle.replace(f"_{days}", "")
        amount = AVAILABLE_BUNDLES[bundle]

        if active_bundle_count > 0 and reserved_bundle_count > 0:
            return JsonResponse({
                'error_msg': "You already have one active and one reserved bundle. Buying more bundles is not possible."
            }, status=403)

        if active_bundle_count > 0:
            new_bundle_is_reserved = True
            current_active_bundle = Bundle.objects.get(cafe_owner=current_cafe_owner, is_active=True)
            if BUNDLE_WEIGHTS[bundle_type] < BUNDLE_WEIGHTS[current_active_bundle.bundle_plan]:
                return JsonResponse({
                    'error_msg': "Sorry, downgrading plans is not possible."
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
            cardNumber = "Not paid yet",
            transId = "Not paid yet",
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
            "factorNumber" : current_transaction.factorNumber,
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


class PayirCallbackView(View):
    def get(self, request, *args, **kwargs):
        status = self.request.GET.get('status')
        token = self.request.GET.get('token')

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
            current_transaction.transId = response["transId"]
            current_transaction.cardNumber = response["cardNumber"]
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

            if current_bundle.is_active:
                return JsonResponse({
                    'msg': "Bundle created and activated"
                }, status=200)
            elif current_bundle.is_reserved:
                return JsonResponse({
                    'msg': "Bundle created and reserved."
                }, status=200)


        else:
            return JsonResponse({
                'error_msg': "Transaction status not 1"
            }, status=403)


class CheckSubscriptionDiscountView(View):
    @permission_decorator_class_based(
        token_authenticate,
        {USER_ROLES['CAFE_OWNER']},
        {USER_PLANS_CHOICES['FREE']},
        branch_disable=True
    )
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        code = rec_data.get('code')
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
        amount = discount_result[0]

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
            }, status=200)
