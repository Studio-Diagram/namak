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


def create_new_invoice_return(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_return_id = rec_data['id']

        if invoice_return_id == 0:
            supplier_id = rec_data['supplier_id']
            shop_id = rec_data['shop_id']
            description = rec_data['description']
            numbers = rec_data['numbers']
            return_type = rec_data['return_type']
            buy_price = rec_data['buy_price']
            username = rec_data['username']
            branch_id = rec_data['branch_id']
            invoice_date = rec_data['date']

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not request.session.get('is_logged_in', None) == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
            if not branch_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not shop_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if supplier_id == 0:
                return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})
            if not numbers:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not description:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not return_type:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not buy_price:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not invoice_date:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            branch_obj = Branch.objects.get(pk=branch_id)
            supplier_obj = Supplier.objects.get(pk=supplier_id)
            shop_obj = ShopProduct.objects.get(pk=shop_id)

            total_price = int(numbers) * int(buy_price)

            invoice_date_split = invoice_date.split('/')
            invoice_date_g = jdatetime.datetime(int(invoice_date_split[2]), int(invoice_date_split[1]),
                                                int(invoice_date_split[0]), datetime.now().hour, datetime.now().minute,
                                                datetime.now().second).togregorian()

            new_invoice = InvoiceReturn(
                branch=branch_obj,
                created_time=invoice_date_g,
                supplier=supplier_obj,
                buy_price=buy_price,
                shop_product=shop_obj,
                description=description,
                numbers=numbers,
                total_price=total_price,
                return_type=return_type
            )
            new_invoice.save()
            
            if return_type == "CUSTOMER_TO_CAFE":
                shop_obj.real_numbers += int(numbers)
                shop_obj.save()
            elif return_type == 'CAFE_TO_SUPPLIER':
                supplier_obj.remainder -= total_price
                supplier_obj.save()
                shop_obj.real_numbers -= int(numbers)
                shop_obj.save()

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
        invoice_objects = InvoiceReturn.objects.filter(branch=branch_obj)
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            invoices.append({
                'id': invoice.pk,
                'supplier_name': invoice.supplier.name,
                'shop_name': invoice.shop_product.name,
                'buy_price': invoice.buy_price,
                'numbers': invoice.numbers,
                'total_price': invoice.numbers * invoice.buy_price,
                'description': invoice.description,
                'date': jalali_date.strftime("%Y/%m/%d")
            })

        return JsonResponse({"response_code": 2, 'invoices': invoices})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_return(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = InvoiceReturn.objects.filter(supplier__name__contains=search_word)
        returns = []
        for invoice_return in items_searched:
            invoice_date = invoice_return.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            returns.append({
                'id': invoice_return.pk,
                'supplier_name': invoice_return.supplier.name,
                'shop_name': invoice_return.shop_product.name,
                'buy_price': invoice_return.buy_price,
                'numbers': invoice_return.numbers,
                'total_price': invoice_return.price,
                'description': invoice_return.description,
                'date': jalali_date.strftime("%Y/%m/%d")
            })
        return JsonResponse({"response_code": 2, 'returns': returns})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def delete_invoice_return(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data['invoice_id']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        invoice_obj = InvoicePurchase.objects.get(pk=invoice_id)
        invoice_type = invoice_obj.settlement_type

        if invoice_type == "CASH":
            invoice_obj.delete()

        elif invoice_type == "CREDIT":
            invoice_obj.supplier.remainder -= invoice_obj.total_price
            invoice_obj.supplier.save()
            invoice_obj.delete()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
