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


class BundleView(View):
    # @permission_decorator_class_based(token_authenticate,
    #                                   {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
    #                                   {},)

    # def get(self, request, *args, **kwargs):


    @permission_decorator_class_based(token_authenticate, {USER_ROLES['CAFE_OWNER']}, {USER_PLANS_CHOICES['FREE']}, branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        bundle = rec_data.get('bundle')
        duration = rec_data.get('duration')
        payload = request.payload

        print(payload)


        if bundle not in AVAILABLE_BUNDLES:
            return JsonResponse({
                'error_msg': BUNDLE_NOT_AVAILABLE
            }, status=400)

        if duration not in AVAILABLE_BUNDLES[bundle]:
            return JsonResponse({
                'error_msg': BUNDLE_DURATION_NOT_AVAILABLE
            }, status=400)

        if duration == '1MONTH':
            days = 30
        elif duration == '3MONTH':
            days = 90
        elif duration == '12MONTH':
            days = 365

        current_cafe_owner = CafeOwner.objects.get(pk=payload['sub_id'])

        current_transaction = Transaction.objects.create(
            cafe_owner = current_cafe_owner,
            status = "Not paid yet",
            token = "No token yet",
            amount = AVAILABLE_BUNDLES[bundle][duration],
            mobile = payload['sub_phone'],
            redirect = settings.PAY_IR_REDIRECT_URL,
            cardNumber = "Not paid yet",
            transId = "Not paid yet",
        )

        current_bundle = Bundle.objects.create(
            bundle_plan = bundle,
            bundle_duration = days,
            starting_datetime_plan = datetime.utcnow(),
            expiry_datetime_plan = datetime.utcnow() + timedelta(days=days, seconds=5),
            is_active = False,
            cafe_owner = current_cafe_owner,
            transaction = current_transaction,
        )

        init_data = {
            "api": settings.PAY_IR_API_KEY,
            "amount" : AVAILABLE_BUNDLES[bundle][duration],
            "redirect": settings.PAY_IR_REDIRECT_URL,
            "factorNumber" : current_transaction.factorNumber,
            "mobile" : payload['sub_phone'],
            'description' : None,
        }
        try:
            response = get_json(requests.post(settings.PAY_IR_API_URL_SEND, data=init_data))
            print(response)
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
            current_bundle.is_active = True
            current_bundle.save()


            return JsonResponse({
                'msg': "Bundle created and activated"
            }, status=200)


        else:
            return JsonResponse({
                'error_msg': "Transaction status not 1"
            }, status=403)
