from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from accountiboard.custom_permissions import *
import json, base64, random, jdatetime
from accounti.models import *
from django.db.models import Q
import accountiboard.settings as settings
from PIL import Image
from io import BytesIO
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta, date
from pytz import timezone
from accountiboard.constants import *


class GetInvoiceNumberView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']})
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_type = rec_data.get('invoice_type')
        branch_id = rec_data.get('branch_id')

        if not invoice_type:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        branch_obj = Branch.objects.filter(id=branch_id).first()

        if invoice_type == "BUY":
            last_invoice_object = InvoicePurchase.objects.filter(branch=branch_obj).order_by('id').last()

        elif invoice_type == "SALE":
            last_invoice_object = InvoiceSales.objects.filter(branch=branch_obj).order_by('id').last()

        elif invoice_type == "RETURN":
            last_invoice_object = InvoiceReturn.objects.filter(branch=branch_obj).order_by('id').last()

        elif invoice_type == "PAY":
            last_invoice_object = InvoiceSettlement.objects.filter(branch=branch_obj).order_by('id').last()

        elif invoice_type == "EXPENSE":
            last_invoice_object = InvoiceExpense.objects.filter(branch=branch_obj).order_by('id').last()

        else:
            return JsonResponse({"response_code": 3, "error_msg": "ERROR 500"})

        if last_invoice_object:
            last_number = last_invoice_object.factor_number
        else:
            last_number = 0

        return JsonResponse({"response_code": 2, "next_factor_number": last_number + 1})
