from django.http import JsonResponse
from django.shortcuts import render
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


def get_invoice_number(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    invoice_type = rec_data['invoice_type']
    username = rec_data['username']
    branch_id = rec_data['branch_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
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
