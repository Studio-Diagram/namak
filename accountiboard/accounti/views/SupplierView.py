from django.http import JsonResponse
import json, jdatetime, xlwt
from datetime import timedelta, datetime
from accounti.models import *
from django.db.models import Sum
from accountiboard import settings
from accountiboard.constants import *


def return_remainder_of_supplier(supplier_id, to_time):
    if not to_time:
        remainder_to_date = datetime.now()
    else:
        to_time_split = to_time.split('/')
        remainder_to_date = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                           int(to_time_split[0])).togregorian() + timedelta(days=1)
    if not supplier_id:
        return False
    supplier_obj = Supplier.objects.filter(id=supplier_id).first()

    # BEDEHKAR
    debtor = 0

    # Credit Invoice Expense
    sum_all_invoice_expense_credit = InvoiceExpense.objects.filter(supplier=supplier_obj,
                                                                   settlement_type="CREDIT",
                                                                   created_time__lte=remainder_to_date).aggregate(
        Sum('price'))
    if sum_all_invoice_expense_credit['price__sum']:
        debtor += sum_all_invoice_expense_credit['price__sum']

    # Credit Invoice Purchase
    sum_all_invoice_purchase_credit = InvoicePurchase.objects.filter(supplier=supplier_obj,
                                                                     settlement_type="CREDIT",
                                                                     created_time__lte=remainder_to_date).aggregate(
        Sum('total_price'))
    if sum_all_invoice_purchase_credit['total_price__sum']:
        debtor += sum_all_invoice_purchase_credit['total_price__sum']

    # Amani Sales
    amani_sale_sum = 0
    all_amani_sales = AmaniSale.objects.filter(supplier=supplier_obj, is_amani=True,
                                               created_date__lte=remainder_to_date)
    for amani_sale in all_amani_sales:
        amani_sale_sum += (amani_sale.numbers - amani_sale.return_numbers) * amani_sale.buy_price

    debtor += amani_sale_sum

    # BESTANKAR
    creditor = 0
    sum_all_invoice_settlement = InvoiceSettlement.objects.filter(supplier=supplier_obj,
                                                                  created_time__lte=remainder_to_date).aggregate(
        Sum('payment_amount'))
    if sum_all_invoice_settlement['payment_amount__sum']:
        creditor += sum_all_invoice_settlement['payment_amount__sum']

    return creditor - debtor


def add_supplier(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    supplier_id = rec_data['id']
    name = rec_data['name']
    phone = rec_data['phone']
    salesman_name = rec_data['salesman_name']
    salesman_phone = rec_data['salesman_phone']
    username = rec_data['username']
    branch_id = rec_data['branch_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not name or not phone or not salesman_name or not salesman_phone or not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    organization_object = Branch.objects.get(id=branch_id).organization

    if supplier_id == 0:
        new_supplier = Supplier(
            name=name,
            phone=phone,
            salesman_name=salesman_name,
            salesman_phone=salesman_phone,
            organization=organization_object
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


def get_suppliers(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data.get('username')
        branch_id = rec_data.get('branch')

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        organization_object = Branch.objects.get(id=branch_id).organization
        suppliers = Supplier.objects.filter(organization=organization_object)
        suppliers_data = []
        for supplier in suppliers:
            jalali_date = ''
            suppliers_data.append({
                'id': supplier.pk,
                'name': supplier.name,
                'phone': supplier.phone,
                'salesman_name': supplier.salesman_name,
                'salesman_phone': supplier.salesman_phone,
                'last_pay': jalali_date,
                'remainder': return_remainder_of_supplier(supplier.id, ""),
            })
        return JsonResponse({"response_code": 2, 'suppliers': suppliers_data})


def search_supplier(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data.get('search_word')
        username = rec_data.get('username')
        branch_id = rec_data.get('branch')

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word or not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        organization_object = Branch.objects.get(id=branch_id).organization
        items_searched = Supplier.objects.filter(name__contains=search_word, organization=organization_object)
        suppliers = []
        for supplier in items_searched:
            jalali_date = ''
            suppliers.append({
                'id': supplier.pk,
                'name': supplier.name,
                'phone': supplier.phone,
                'salesman_name': supplier.salesman_name,
                'salesman_phone': supplier.salesman_phone,
                'last_pay': jalali_date,
                'remainder': return_remainder_of_supplier(supplier.id, ""),
            })
        return JsonResponse({"response_code": 2, 'suppliers': suppliers})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_supplier(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    supplier_id = rec_data['supplier_id']

    supplier = Supplier.objects.get(pk=supplier_id)
    supplier_data = {
        'id': supplier.pk,
        'name': supplier.name,
        'phone': supplier.phone,
        'salesman_name': supplier.salesman_name,
        'salesman_phone': supplier.salesman_phone,
        'remainder': return_remainder_of_supplier(supplier.id, "")
    }
    return JsonResponse({"response_code": 2, 'supplier': supplier_data})


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
                                       int(to_time_split[0])).togregorian() + timedelta(days=1)
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
                                       int(to_time_split[0])).togregorian() + timedelta(days=1)
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
                                       int(to_time_split[0])).togregorian() + timedelta(days=1)
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
                                       int(to_time_split[0])).togregorian() + timedelta(days=1)
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
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch']
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
                                   int(to_time_split[0])).togregorian() + timedelta(days=1)
        all_amani_sales_from_supplier = AmaniSale.objects.filter(supplier=supplier,
                                                                 created_date__range=(from_time_g, to_time_g))
        all_amani_sum = 0
        all_amani_buy = 0
        for amani_sale in all_amani_sales_from_supplier:
            all_amani_buy += amani_sale.numbers
            all_amani_sum += amani_sale.numbers * amani_sale.buy_price

        return JsonResponse(
            {"response_code": 2, 'all_amani_sales_sum': all_amani_sum, 'all_amani_sales_buy': all_amani_buy})


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
                                       int(to_time_split[0])).togregorian() + timedelta(days=1)
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
                                       int(to_time_split[0])).togregorian() + timedelta(days=1)
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
                                       int(to_time_split[0])).togregorian() + timedelta(days=1)
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
                                       int(to_time_split[0])).togregorian() + timedelta(days=1)
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
                    'price': invoice.total_price,
                    'date': jalali_date.strftime("%Y/%m/%d")
                })

            if not all_invoice_returns_sum['total_price__sum']:
                all_invoice_returns_sum['total_price__sum'] = 0
            return JsonResponse({"response_code": 2, 'invoices_data': invoices_data,
                                 'all_invoice_returns_sum': all_invoice_returns_sum['total_price__sum']})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_detail_amani_sales_from_supplier(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')
    from_time = rec_data.get('from_time')
    to_time = rec_data.get('to_time')
    supplier_id = rec_data.get('supplier_id')

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not supplier_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    supplier = Supplier.objects.get(pk=supplier_id)

    if from_time == "" or to_time == "":
        all_amani_sales_from_supplier = AmaniSale.objects.filter(supplier=supplier).order_by('-created_date')
        all_amani_sum = 0

        invoices_data = []
        amani_sale_base_on_product = {}
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

            shop_product_name = amani_sale.invoice_sale_to_shop.shop_product.name
            if shop_product_name in amani_sale_base_on_product:
                amani_sale_base_on_product[shop_product_name]['price'] += \
                    (amani_sale.numbers - amani_sale.return_numbers) * amani_sale.buy_price
                amani_sale_base_on_product[shop_product_name]['numbers'] += amani_sale.numbers
                amani_sale_base_on_product[shop_product_name]['return_numbers'] += amani_sale.return_numbers
            else:
                amani_sale_base_on_product[shop_product_name] = {
                    'price': (amani_sale.numbers - amani_sale.return_numbers) * amani_sale.buy_price,
                    'numbers': amani_sale.numbers,
                    'name': amani_sale.invoice_sale_to_shop.shop_product.name,
                    'sale_price': amani_sale.sale_price,
                    'buy_price': amani_sale.buy_price,
                    'return_numbers': amani_sale.return_numbers,
                }

        return JsonResponse(
            {"response_code": 2, 'all_invoice_amani_sales_sum': all_amani_sum, 'invoices_data': invoices_data,
             'amani_sale_base_on_product': amani_sale_base_on_product})

    elif from_time and to_time:
        from_time_split = from_time.split('/')
        from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                     int(from_time_split[0])).togregorian()
        to_time_split = to_time.split('/')
        to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                                   int(to_time_split[0])).togregorian() + timedelta(days=1)
        all_amani_sales_from_supplier = AmaniSale.objects.filter(supplier=supplier,
                                                                 created_date__range=(
                                                                     from_time_g, to_time_g)).order_by(
            '-created_date')
        all_amani_sum = 0
        invoices_data = []
        amani_sale_base_on_product = {}
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
            shop_product_name = amani_sale.invoice_sale_to_shop.shop_product.name
            if shop_product_name in amani_sale_base_on_product:
                amani_sale_base_on_product[shop_product_name]['price'] += \
                    (amani_sale.numbers - amani_sale.return_numbers) * amani_sale.buy_price
                amani_sale_base_on_product[shop_product_name]['numbers'] += amani_sale.numbers
                amani_sale_base_on_product[shop_product_name]['return_numbers'] += amani_sale.return_numbers
            else:
                amani_sale_base_on_product[shop_product_name] = {
                    'price': (amani_sale.numbers - amani_sale.return_numbers) * amani_sale.buy_price,
                    'numbers': amani_sale.numbers,
                    'name': amani_sale.invoice_sale_to_shop.shop_product.name,
                    'sale_price': amani_sale.sale_price,
                    'buy_price': amani_sale.buy_price,
                    'return_numbers': amani_sale.return_numbers,
                }

        return JsonResponse(
            {"response_code": 2, 'all_invoice_amani_sales_sum': all_amani_sum, 'invoices_data': invoices_data,
             'amani_sale_base_on_product': amani_sale_base_on_product})


def get_remainder_supplier(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    to_time = rec_data['to_time']
    supplier_id = rec_data['supplier_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    supplier_remainder = return_remainder_of_supplier(supplier_id, to_time)
    return JsonResponse(
        {"response_code": 2, 'supplier_remainder': supplier_remainder})


def create_all_supplier_excel(request):
    rec_data = json.loads(request.read().decode('utf-8'))
    from_time = rec_data['from_time']
    to_time = rec_data['to_time']

    from_time_split = from_time.split('/')
    from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                 int(from_time_split[0])).togregorian()
    to_time_split = to_time.split('/')
    to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                               int(to_time_split[0])).togregorian()

    all_suppliers = Supplier.objects.all()
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('all_suppliers')
    row = 0

    for supplier in all_suppliers:
        row += 3
        all_invoice_purchase = InvoicePurchase.objects.filter(supplier=supplier,
                                                              created_time__lte=to_time_g,
                                                              created_time__gte=from_time_g)

        for invoice_purchase in all_invoice_purchase:
            invoice_data = []
            invoice_date = invoice_purchase.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            jalali_date = jalali_date.strftime("%Y/%m/%d")
            invoice_data.append("فاکتور خرید")
            invoice_data.append(invoice_purchase.factor_number)
            invoice_data.append(jalali_date)
            invoice_data.append(invoice_purchase.supplier.name)
            invoice_data.append(invoice_purchase.settlement_type)
            invoice_data.append(invoice_purchase.total_price)
            invoice_data.append(invoice_purchase.tax)
            invoice_data.append(invoice_purchase.discount)
            invoice_data.append(invoice_purchase.branch.name)

            for col in range(len(invoice_data)):
                sheet.write(row, col, invoice_data[col])
            row += 1

        row += 1

        all_invoice_settlement = InvoiceSettlement.objects.filter(supplier=supplier,
                                                                  created_time__lte=to_time_g,
                                                                  created_time__gte=from_time_g)

        for invoice_settlement in all_invoice_settlement:
            invoice_data = []
            invoice_date = invoice_settlement.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            jalali_date = jalali_date.strftime("%Y/%m/%d")
            invoice_data.append("فاکتور پرداختی")
            invoice_data.append(invoice_settlement.factor_number)
            invoice_data.append(jalali_date)
            invoice_data.append(invoice_settlement.supplier.name)
            invoice_data.append(invoice_settlement.get_settle_type_display())
            invoice_data.append(invoice_settlement.payment_amount)
            invoice_data.append(invoice_settlement.tax)
            invoice_data.append(invoice_settlement.discount)
            invoice_data.append(invoice_settlement.backup_code)
            invoice_data.append(invoice_settlement.branch.name)

            for col in range(len(invoice_data)):
                sheet.write(row, col, invoice_data[col])
            row += 1

        row += 1
        all_invoice_return = InvoiceReturn.objects.filter(supplier=supplier, created_time__lte=to_time_g,
                                                          created_time__gte=from_time_g)

        for invoice_return in all_invoice_return:
            invoice_data = []
            invoice_date = invoice_return.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            jalali_date = jalali_date.strftime("%Y/%m/%d")
            invoice_data.append("فاکتور مرجوعی")
            invoice_data.append(invoice_return.factor_number)
            invoice_data.append(jalali_date)
            invoice_data.append(invoice_return.supplier.name)
            invoice_data.append(invoice_return.get_return_type_display())
            invoice_data.append(invoice_return.total_price)
            invoice_data.append(invoice_return.numbers)
            invoice_data.append(invoice_return.shop_product.name)
            invoice_data.append(invoice_return.description)
            invoice_data.append(invoice_return.branch.name)

            for col in range(len(invoice_data)):
                sheet.write(row, col, invoice_data[col])
            row += 1

        row += 1
        all_invoice_expense = InvoiceExpense.objects.filter(supplier=supplier, created_time__gte=from_time_g,
                                                            created_time__lte=to_time_g)

        for invoice_expense in all_invoice_expense:
            invoice_data = []
            invoice_date = invoice_expense.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            jalali_date = jalali_date.strftime("%Y/%m/%d")
            invoice_data.append("فاکتور هزینه")
            invoice_data.append(invoice_expense.factor_number)
            invoice_data.append(jalali_date)
            invoice_data.append(invoice_expense.supplier.name)
            invoice_data.append(invoice_expense.get_expense_kind_display())
            invoice_data.append(invoice_expense.get_settlement_type_display())
            invoice_data.append(invoice_expense.price)
            invoice_data.append(invoice_expense.tax)
            invoice_data.append(invoice_expense.discount)
            invoice_data.append(invoice_expense.branch.name)

            for col in range(len(invoice_data)):
                sheet.write(row, col, invoice_data[col])
            row += 1

        row += 1
        all_amani_sales = AmaniSale.objects.filter(supplier=supplier, created_date__gte=from_time_g,
                                                   created_date__lte=to_time_g)

        for amani_sale in all_amani_sales:
            invoice_data = []
            invoice_date = amani_sale.created_date.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            jalali_date = jalali_date.strftime("%Y/%m/%d")
            invoice_data.append("فروش امانی")
            invoice_data.append(amani_sale.id)
            invoice_data.append(jalali_date)
            invoice_data.append(amani_sale.supplier.name)
            invoice_data.append(amani_sale.numbers)
            invoice_data.append(amani_sale.numbers * amani_sale.buy_price)
            invoice_data.append(amani_sale.invoice_sale_to_shop.shop_product.name)
            invoice_data.append(amani_sale.invoice_sale_to_shop.invoice_sales.branch.name)

            for col in range(len(invoice_data)):
                sheet.write(row, col, invoice_data[col])
            row += 1

    excel_name = 'all_suppliers_%s.xls' % str(datetime.datetime.now())
    workbook.save(settings.MEDIA_ROOT + "/" + excel_name)

    return JsonResponse(
        {"response_code": 2, 'file_name': excel_name})


def create_all_materials_buy(request):
    rec_data = json.loads(request.read().decode('utf-8'))
    from_time = rec_data['from_time']
    to_time = rec_data['to_time']

    from_time_split = from_time.split('/')
    from_time_g = jdatetime.date(int(from_time_split[2]), int(from_time_split[1]),
                                 int(from_time_split[0])).togregorian()
    to_time_split = to_time.split('/')
    to_time_g = jdatetime.date(int(to_time_split[2]), int(to_time_split[1]),
                               int(to_time_split[0])).togregorian()

    all_invoice_purchase_to_material = PurchaseToMaterial.objects.filter(
        invoice_purchase__created_time__gte=from_time_g, invoice_purchase__created_time__lte=to_time_g).order_by(
        'invoice_purchase__created_time')
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('all_suppliers')
    row = 0

    for purchase_to_material in all_invoice_purchase_to_material:
        row += 1
        data = []
        data.append(purchase_to_material.invoice_purchase.factor_number)
        invoice_date = purchase_to_material.invoice_purchase.created_time.date()
        jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                   year=invoice_date.year)
        jalali_date = jalali_date.strftime("%Y/%m/%d")
        data.append(jalali_date)
        data.append(purchase_to_material.material.name)
        data.append(purchase_to_material.unit_numbers)
        data.append(purchase_to_material.base_unit_price)
        data.append(purchase_to_material.unit_numbers * purchase_to_material.base_unit_price)
        for col in range(len(data)):
            sheet.write(row, col, data[col])

    excel_name = 'all_materials_%s.xls' % str(datetime.datetime.now())
    workbook.save(settings.MEDIA_ROOT + "/" + excel_name)
    return JsonResponse(
        {"response_code": 2, 'file_name': excel_name})


def get_supplier_purchase_item_used(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    supplier_id = rec_data['supplier_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    if not supplier_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    favourite_materials = []
    favourite_shop_products = []

    materials = PurchaseToMaterial.objects.filter(invoice_purchase__supplier=supplier_id).values("material__pk",
                                                                                                 "material__name",
                                                                                                 "material__unit").distinct()
    for material in materials:
        last_material = PurchaseToMaterial.objects.filter(material=material['material__pk']).last()
        favourite_materials.append({
            "id": material['material__pk'],
            "name": material['material__name'],
            "unit": material['material__unit'],
            "price": last_material.base_unit_price
        })

    shop_products = PurchaseToShopProduct.objects.filter(invoice_purchase__supplier=supplier_id).values(
        "shop_product__pk",
        "shop_product__name",
        "shop_product__price").distinct()

    for shop_p in shop_products:
        last_shop_p = PurchaseToShopProduct.objects.filter(shop_product=shop_p['shop_product__pk']).last()
        favourite_shop_products.append({
            "id": shop_p['shop_product__pk'],
            "name": shop_p['shop_product__name'],
            "price": shop_p['shop_product__price'],
            "buy_price": last_shop_p.base_unit_price
        })

    return JsonResponse(
        {"response_code": 2, 'materials': favourite_materials, "shop_products": favourite_shop_products})
