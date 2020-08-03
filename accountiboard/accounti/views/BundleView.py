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
        duration = rec_data.get('duration')
        discount_code = rec_data.get('discount_code')
        payload = request.payload

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

        days = RE_DURATION.findall(bundle)[0]

        current_cafe_owner = CafeOwner.objects.get(pk=payload['sub_id'])
        active_bundle_count = Bundle.objects.filter(cafe_owner=current_cafe_owner, is_active=True).count()

        if active_bundle_count > 0:
            new_bundle_is_reserved = True
        else:
            new_bundle_is_reserved = False

        amount = AVAILABLE_BUNDLES[bundle]

        # if discount_code:
        #     if current_discount_obj.type == 'amount':
        #         amount = AVAILABLE_BUNDLES[bundle][duration] - current_discount_obj.quantity
        #     elif current_discount_obj.type == 'percent':
        #         amount = AVAILABLE_BUNDLES[bundle][duration] - current_discount_obj.quantity * AVAILABLE_BUNDLES[bundle][duration]
        # else:
        #     amount = AVAILABLE_BUNDLES[bundle][duration]



        current_transaction = Transaction.objects.create(
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
            bundle_plan = bundle.replace(f"_{days}", ""),
            bundle_duration = days,
            starting_datetime_plan = datetime.utcnow(),
            expiry_datetime_plan = datetime.utcnow() + timedelta(days=int(days), seconds=5),
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

        try:
            subscription_discount = SubscriptionDiscount.objects.get(code=code)
            return JsonResponse({
                'msg': "subscription discount code is valid.",
                'type': subscription_discount.type,
                'name': subscription_discount.name,
                'quantity': subscription_discount.quantity,
            }, status=200)

        except:
            return JsonResponse({
                'msg': "subscription discount code is not valid."
            }, status=200)



