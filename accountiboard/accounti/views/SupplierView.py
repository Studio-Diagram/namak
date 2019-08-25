from django.http import JsonResponse
import json, jdatetime
from accounti.models import *
from django.db.models import Sum

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'


def add_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        supplier_id = rec_data['id']
        name = rec_data['name']
        phone = rec_data['phone']
        salesman_name = rec_data['salesman_name']
        salesman_phone = rec_data['salesman_phone']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not phone:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not salesman_name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not salesman_phone:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if supplier_id == 0:
            new_supplier = Supplier(
                name=name,
                phone=phone,
                salesman_name=salesman_name,
                salesman_phone=salesman_phone,
            )
            new_supplier.save()

            return JsonResponse({"response_code": 2})
        else:
            ol_supplier = Supplier.objects.get(pk=supplier_id)
            ol_supplier.name = name
            ol_supplier.phone = phone
            ol_supplier.salesman_name = salesman_name
            ol_supplier.salesman_phone = salesman_phone
            ol_supplier.save()
            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_suppliers(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        suppliers = Supplier.objects.all()
        suppliers_data = []
        for supplier in suppliers:
            jalali_date = ''
            if supplier.last_pay:
                last_pay_date = supplier.last_pay
                jalali_date = jdatetime.date.fromgregorian(day=last_pay_date.day, month=last_pay_date.month,
                                                           year=last_pay_date.year)
                jalali_date = jalali_date.strftime("%Y/%m/%d")
            suppliers_data.append({
                'id': supplier.pk,
                'name': supplier.name,
                'phone': supplier.phone,
                'salesman_name': supplier.salesman_name,
                'salesman_phone': supplier.salesman_phone,
                'last_pay': jalali_date,
                'remainder': supplier.remainder,
            })
        return JsonResponse({"response_code": 2, 'suppliers': suppliers_data})


def search_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Supplier.objects.filter(name__contains=search_word)
        suppliers = []
        for supplier in items_searched:
            jalali_date = ''
            if supplier.last_pay:
                last_pay_date = supplier.last_pay
                jalali_date = jdatetime.date.fromgregorian(day=last_pay_date.day, month=last_pay_date.month,
                                                           year=last_pay_date.year)
                jalali_date = jalali_date.strftime("%Y/%m/%d")
            suppliers.append({
                'id': supplier.pk,
                'name': supplier.name,
                'phone': supplier.phone,
                'salesman_name': supplier.salesman_name,
                'salesman_phone': supplier.salesman_phone,
                'last_pay': jalali_date,
                'remainder': supplier.remainder,
            })
        return JsonResponse({"response_code": 2, 'suppliers': suppliers})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            supplier_id = rec_data['supplier_id']

            supplier = Supplier.objects.get(pk=supplier_id)
            supplier_data = {
                'id': supplier.pk,
                'name': supplier.name,
                'phone': supplier.phone,
                'salesman_name': supplier.salesman_name,
                'salesman_phone': supplier.salesman_phone,
                'remainder': supplier.remainder,
            }
            return JsonResponse({"response_code": 2, 'supplier': supplier_data})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_sum_invoice_purchases_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        supplier = Supplier.objects.get(pk=supplier_id)
        last_buy = supplier.last_buy
        if last_buy:
            jalali_date = jdatetime.date.fromgregorian(day=last_buy.day, month=last_buy.month, year=last_buy.year)
            purchase_date = jalali_date.strftime("%Y/%m/%d")
        else:
            purchase_date = ''

        if from_time == "" or to_time == "":
            all_invoice_purchases = InvoicePurchase.objects.filter(supplier=supplier)
            all_invoice_purchases_sum = all_invoice_purchases.aggregate(Sum('total_price'))
            purchase_count = all_invoice_purchases.count()
            if not all_invoice_purchases_sum['total_price__sum']:
                all_invoice_purchases_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'all_invoice_purchases_sum': all_invoice_purchases_sum,
                                 'last_buy': purchase_date, 'purchase_count': purchase_count})

        elif from_time and to_time:
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_invoice_purchases = InvoicePurchase.objects.filter(supplier=supplier,
                                                                   created_time__range=(from_time_g, to_time_g))
            all_invoice_purchases_sum = all_invoice_purchases.aggregate(Sum('total_price'))
            purchase_count = all_invoice_purchases.count()
            if not all_invoice_purchases_sum['total_price__sum']:
                all_invoice_purchases_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'all_invoice_purchases_sum': all_invoice_purchases_sum,
                                 'last_buy': purchase_date, 'purchase_count': purchase_count})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_sum_invoice_settlements_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        supplier = Supplier.objects.get(pk=supplier_id)
        last_pay = supplier.last_pay
        if last_pay:
            jalali_date = jdatetime.date.fromgregorian(day=last_pay.day, month=last_pay.month,
                                                       year=last_pay.year)
            pay_date = jalali_date.strftime("%Y/%m/%d")
        else:
            pay_date = ''

        if from_time == "" or to_time == "":
            all_invoice_settlements = InvoiceSettlement.objects.filter(supplier=supplier)
            all_invoice_settlements_sum = all_invoice_settlements.aggregate(Sum('payment_amount'))
            pay_count = all_invoice_settlements.count()
            if not all_invoice_settlements_sum['payment_amount__sum']:
                all_invoice_settlements_sum['payment_amount__sum'] = 0
            return JsonResponse({"response_code": 2, 'all_invoice_settlements_sum': all_invoice_settlements_sum,
                                 'last_pay': pay_date, 'pay_count': pay_count})

        elif from_time and to_time:
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_invoice_settlements = InvoiceSettlement.objects.filter(supplier=supplier,
                                                                       created_time__range=(from_time_g, to_time_g))
            all_invoice_settlements_sum = all_invoice_settlements.aggregate(Sum('payment_amount'))
            purchase_count = all_invoice_settlements.count()
            if not all_invoice_settlements_sum['payment_amount__sum']:
                all_invoice_settlements_sum['payment_amount__sum'] = 0
            return JsonResponse({"response_code": 2, 'all_invoice_settlements_sum': all_invoice_settlements_sum,
                                 'last_pay': pay_date, 'pay_count': purchase_count})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_sum_invoice_expenses_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        supplier = Supplier.objects.get(pk=supplier_id)
        last_expense = supplier.last_expense
        if last_expense:
            jalali_date = jdatetime.date.fromgregorian(day=last_expense.day, month=last_expense.month,
                                                       year=last_expense.year)
            expense_date = jalali_date.strftime("%Y/%m/%d")
        else:
            expense_date = ''

        if from_time == "" or to_time == "":
            all_invoice_expenses = InvoiceExpense.objects.filter(supplier=supplier)
            all_invoice_expenses_sum = all_invoice_expenses.aggregate(Sum('price'))
            all_invoice_expenses_count = all_invoice_expenses.count()
            if not all_invoice_expenses_sum['price__sum']:
                all_invoice_expenses_sum['price__sum'] = 0
            return JsonResponse({"response_code": 2, 'all_invoice_expenses_sum': all_invoice_expenses_sum,
                                 'last_expense': expense_date, 'expense_count': all_invoice_expenses_count})

        elif from_time and to_time:
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_invoice_expenses = InvoiceExpense.objects.filter(supplier=supplier,
                                                                 created_time__range=(from_time_g, to_time_g))
            all_invoice_expenses_sum = all_invoice_expenses.aggregate(Sum('price'))
            purchase_count = all_invoice_expenses.count()
            if not all_invoice_expenses_sum['price__sum']:
                all_invoice_expenses_sum['price__sum'] = 0
            return JsonResponse({"response_code": 2, 'all_invoice_expenses_sum': all_invoice_expenses_sum,
                                 'last_expense': expense_date, 'expense_count': purchase_count})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_sum_invoice_return_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        supplier = Supplier.objects.get(pk=supplier_id)
        last_return = supplier.last_return
        if last_return:
            jalali_date = jdatetime.date.fromgregorian(day=last_return.day, month=last_return.month,
                                                       year=last_return.year)
            return_date = jalali_date.strftime("%Y/%m/%d")
        else:
            return_date = ''

        if from_time == "" or to_time == "":
            all_invoice_returns = InvoiceReturn.objects.filter(supplier=supplier, return_type="CAFE_TO_SUPPLIER")
            all_invoice_returns_sum = all_invoice_returns.aggregate(Sum('total_price'))
            all_invoice_returns_count = all_invoice_returns.count()
            if not all_invoice_returns_sum['total_price__sum']:
                all_invoice_returns_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'all_invoice_returns_sum': all_invoice_returns_sum,
                                 'last_return': return_date, 'return_count': all_invoice_returns_count})

        elif from_time and to_time:
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_invoice_returns = InvoiceReturn.objects.filter(supplier=supplier,
                                                               created_time__range=(from_time_g, to_time_g),
                                                               return_type="CAFE_TO_SUPPLIER")
            all_invoice_returns_sum = all_invoice_returns.aggregate(Sum('total_price'))
            purchase_count = all_invoice_returns.count()
            if not all_invoice_returns_sum['total_price__sum']:
                all_invoice_returns_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'all_invoice_returns_sum': all_invoice_returns_sum,
                                 'last_return': return_date, 'return_count': purchase_count})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_sum_amani_sales_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        supplier = Supplier.objects.get(pk=supplier_id)
        if from_time == "" or to_time == "":
            all_amani_sales_from_supplier = AmaniSale.objects.filter(supplier=supplier)
            all_amani_sum = 0
            all_amani_buy = 0
            for amani_sale in all_amani_sales_from_supplier:
                all_amani_buy += amani_sale.numbers
                all_amani_sum += (amani_sale.numbers - amani_sale.return_numbers) * amani_sale.buy_price

            return JsonResponse(
                {"response_code": 2, 'all_amani_sales_sum': all_amani_sum, 'all_amani_sales_buy': all_amani_buy})

        elif from_time and to_time:
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_amani_sales_from_supplier = AmaniSale.objects.filter(supplier=supplier,
                                                                     created_date__range=(from_time_g, to_time_g))
            all_amani_sum = 0
            all_amani_buy = 0
            for amani_sale in all_amani_sales_from_supplier:
                all_amani_buy += amani_sale.numbers
                all_amani_sum += amani_sale.numbers * amani_sale.buy_price

            return JsonResponse(
                {"response_code": 2, 'all_amani_sales_sum': all_amani_sum, 'all_amani_sales_buy': all_amani_buy})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_detail_invoice_purchases_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if from_time == "" or to_time == "":
            supplier = Supplier.objects.get(pk=supplier_id)
            all_invoice_purchases = InvoicePurchase.objects.filter(supplier=supplier)
            all_invoice_purchases_sum = all_invoice_purchases.aggregate(Sum('total_price'))
            invoices_data = []
            for invoice in all_invoice_purchases:
                date = invoice.created_time.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': invoice.pk,
                    'tax': invoice.tax,
                    'discount': invoice.discount,
                    'kind': invoice.get_settlement_type_display(),
                    'price': invoice.total_price,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_purchases_sum['total_price__sum']:
                all_invoice_purchases_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_purchases_sum': all_invoice_purchases_sum['total_price__sum']})

        elif from_time and to_time:
            supplier = Supplier.objects.get(pk=supplier_id)
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_invoice_purchases = InvoicePurchase.objects.filter(supplier=supplier,
                                                                   created_time__range=(from_time_g, to_time_g))
            all_invoice_purchases_sum = all_invoice_purchases.aggregate(Sum('total_price'))
            invoices_data = []
            for invoice in all_invoice_purchases:
                date = invoice.created_time.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': invoice.pk,
                    'tax': invoice.tax,
                    'discount': invoice.discount,
                    'kind': invoice.get_settlement_type_display(),
                    'price': invoice.total_price,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_purchases_sum['total_price__sum']:
                all_invoice_purchases_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_purchases_sum': all_invoice_purchases_sum['total_price__sum']})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_detail_invoice_expenses_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if from_time == "" or to_time == "":
            supplier = Supplier.objects.get(pk=supplier_id)
            all_invoice_expenses = InvoiceExpense.objects.filter(supplier=supplier)
            all_invoice_expenses_sum = all_invoice_expenses.aggregate(Sum('price'))
            invoices_data = []
            for invoice in all_invoice_expenses:
                date = invoice.created_time.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': invoice.pk,
                    'tax': invoice.tax,
                    'discount': invoice.discount,
                    'kind': invoice.get_settlement_type_display(),
                    'price': invoice.price,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_expenses_sum['price__sum']:
                all_invoice_expenses_sum['price__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_expenses_sum': all_invoice_expenses_sum['price__sum']})

        elif from_time and to_time:
            supplier = Supplier.objects.get(pk=supplier_id)
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_invoice_expenses = InvoiceExpense.objects.filter(supplier=supplier,
                                                                 created_time__range=(from_time_g, to_time_g))
            all_invoice_expenses_sum = all_invoice_expenses.aggregate(Sum('price'))
            invoices_data = []
            for invoice in all_invoice_expenses:
                date = invoice.created_time.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': invoice.pk,
                    'tax': invoice.tax,
                    'discount': invoice.discount,
                    'kind': invoice.get_settlement_type_display(),
                    'price': invoice.price,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_expenses_sum['total_price__sum']:
                all_invoice_expenses_sum['price__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_expenses_sum': all_invoice_expenses_sum['price__sum']})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_detail_invoice_settlements_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if from_time == "" or to_time == "":
            supplier = Supplier.objects.get(pk=supplier_id)
            all_invoice_settlements = InvoiceSettlement.objects.filter(supplier=supplier)
            all_invoice_settlements_sum = all_invoice_settlements.aggregate(Sum('payment_amount'))
            invoices_data = []
            for invoice in all_invoice_settlements:
                date = invoice.created_time.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': invoice.pk,
                    'tax': invoice.tax,
                    'discount': invoice.discount,
                    'kind': 'پرداخت',
                    'price': invoice.payment_amount,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_settlements_sum['payment_amount__sum']:
                all_invoice_settlements_sum['payment_amount__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_settlements_sum': all_invoice_settlements_sum['payment_amount__sum']})

        elif from_time and to_time:
            supplier = Supplier.objects.get(pk=supplier_id)
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_invoice_settlements = InvoiceSettlement.objects.filter(supplier=supplier,
                                                                       created_time__range=(from_time_g, to_time_g))
            all_invoice_settlements_sum = all_invoice_settlements.aggregate(Sum('payment_amount'))
            invoices_data = []
            for invoice in all_invoice_settlements:
                date = invoice.created_time.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': invoice.pk,
                    'tax': invoice.tax,
                    'discount': invoice.discount,
                    'kind': 'پرداخت',
                    'price': invoice.payment_amount,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_settlements_sum['payment_amount__sum']:
                all_invoice_settlements_sum['payment_amount__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_settlements_sum': all_invoice_settlements_sum['payment_amount__sum']})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_detail_invoice_returns_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if from_time == "" or to_time == "":
            supplier = Supplier.objects.get(pk=supplier_id)
            all_invoice_returns = InvoiceReturn.objects.filter(supplier=supplier, return_type="CAFE_TO_SUPPLIER")
            all_invoice_returns_sum = all_invoice_returns.aggregate(Sum('total_price'))
            invoices_data = []
            for invoice in all_invoice_returns:
                date = invoice.created_time.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': invoice.pk,
                    'tax': 0,
                    'discount': 0,
                    'kind': 'مرجوعی',
                    'price': invoice.total_price,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_returns_sum['total_price__sum']:
                all_invoice_returns_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_returns_sum': all_invoice_returns_sum['total_price__sum']})

        elif from_time and to_time:
            supplier = Supplier.objects.get(pk=supplier_id)
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_invoice_returns = InvoiceReturn.objects.filter(supplier=supplier,
                                                               created_time__range=(from_time_g, to_time_g),
                                                               return_type="CAFE_TO_SUPPLIER")
            all_invoice_returns_sum = all_invoice_returns.aggregate(Sum('total_price'))
            invoices_data = []
            for invoice in all_invoice_returns:
                date = invoice.created_time.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': invoice.pk,
                    'tax': 0,
                    'discount': 0,
                    'kind': 'مرجوعی',
                    'price': invoice.numbers * invoice.buy_price,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_returns_sum['total_price__sum']:
                all_invoice_returns_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_returns_sum': all_invoice_returns_sum['total_price__sum']})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_detail_amani_sales_from_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        from_time = rec_data['from_time']
        to_time = rec_data['to_time']
        supplier_id = rec_data['supplier_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not supplier_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        supplier = Supplier.objects.get(pk=supplier_id)

        if from_time == "" or to_time == "":
            all_amani_sales_from_supplier = AmaniSale.objects.filter(supplier=supplier)
            all_amani_sum = 0

            invoices_data = []
            for amani_sale in all_amani_sales_from_supplier:
                all_amani_sum += (amani_sale.numbers - amani_sale.return_numbers) * amani_sale.buy_price
                date = amani_sale.created_date.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': amani_sale.invoice_sale_to_shop.invoice_sales.pk,
                    'price': amani_sale.numbers * amani_sale.buy_price,
                    'numbers': amani_sale.numbers,
                    'name': amani_sale.invoice_sale_to_shop.shop_product.name,
                    'sale_price': amani_sale.sale_price,
                    'buy_price': amani_sale.buy_price,
                    'return_numbers': amani_sale.return_numbers,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            return JsonResponse(
                {"response_code": 2, 'all_invoice_amani_sales_sum': all_amani_sum, 'invoices_data': invoices_data})

        elif from_time and to_time:
            from_time_split = from_time.split('/')
            from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                         int(from_time_split[0])).togregorian()
            to_time_split = to_time.split('/')
            to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                       int(to_time_split[0]) + 1).togregorian()
            all_amani_sales_from_supplier = AmaniSale.objects.filter(supplier=supplier,
                                                                     created_date__range=(from_time_g, to_time_g))
            all_amani_sum = 0
            invoices_data = []
            for amani_sale in all_amani_sales_from_supplier:
                all_amani_sum += amani_sale.numbers * amani_sale.buy_price
                date = amani_sale.created_date.date()
                jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month,
                                                           year=date.year)
                invoices_data.append({
                    'invoice_id': amani_sale.invoice_sale_to_shop.invoice_sales.pk,
                    'price': amani_sale.numbers * amani_sale.buy_price,
                    'numbers': amani_sale.numbers,
                    'name': amani_sale.invoice_sale_to_shop.shop_product.name,
                    'sale_price': amani_sale.sale_price,
                    'buy_price': amani_sale.buy_price,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            return JsonResponse(
                {"response_code": 2, 'all_invoice_amani_sales_sum': all_amani_sum, 'invoices_data': invoices_data})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
