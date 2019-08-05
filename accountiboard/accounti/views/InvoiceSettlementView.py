from django.http import JsonResponse
from accounti.models import *
from datetime import datetime
import jdatetime, json

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
SUPPLIER_REQUIRE = "تامین کننده وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'


def create_new_invoice_settlement(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_settlement_id = rec_data['id']

        if invoice_settlement_id == 0:
            supplier_id = rec_data['supplier_id']
            payment_amount = rec_data['payment_amount']
            username = rec_data['username']
            branch_id = rec_data['branch_id']

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not request.session.get('is_logged_in', None) == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
            if not branch_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not payment_amount:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if supplier_id == 0:
                return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})

            branch_obj = Branch.objects.get(pk=branch_id)
            supplier_obj = Supplier.objects.get(pk=supplier_id)
            now_time = datetime.now()

            new_invoice = InvoiceSettlement(
                branch=branch_obj,
                payment_amount=payment_amount,
                supplier=supplier_obj,
                created_time=now_time
            )
            new_invoice.save()

            supplier_obj.remainder -= int(payment_amount)
            supplier_obj.last_pay = now_time
            supplier_obj.save()

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 3, "error_msg": "Wrong ID!"})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_all_invoices(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        invoice_objects = InvoiceSettlement.objects.filter(branch=branch_obj)
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            invoices.append({
                'id': invoice.pk,
                'supplier_name': invoice.supplier.name,
                'payment_amount': invoice.payment_amount,
                'created_time': jalali_date.strftime("%Y/%m/%d")
            })

        return JsonResponse({"response_code": 2, 'invoices': invoices})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_pays(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = InvoiceSettlement.objects.filter(supplier__name__contains=search_word)
        pays = []
        for pay in items_searched:
            invoice_date = pay.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            pays.append({
                'id': pay.pk,
                'supplier_name': pay.supplier.name,
                'payment_amount': pay.payment_amount,
                'created_time': jalali_date.strftime("%Y/%m/%d")
            })
        return JsonResponse({"response_code": 2, 'pays': pays})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def delete_invoice_settlement(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data['invoice_id']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        invoice_obj = InvoiceSettlement.objects.get(pk=invoice_id)

        invoice_obj.supplier.remainder += invoice_obj.payment_amount
        invoice_obj.supplier.save()
        invoice_obj.delete()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})