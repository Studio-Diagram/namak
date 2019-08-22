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

UNAUTHENTICATED = 'لطفا ابتدا وارد شوید.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."


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
        last_purchase_id = InvoicePurchase.objects.filter(branch=branch_obj).order_by('id').last().factor_number

        return JsonResponse({"response_code": 2, "next_factor_number": last_purchase_id + 1})
