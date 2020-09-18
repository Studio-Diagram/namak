from django.http import JsonResponse
from django.views import View
from accountiboard.custom_permissions import *
from accounti.models import *
from datetime import datetime
import jdatetime, json
from django.db.models import Sum
from accountiboard.constants import *


def get_detail_product_number(shop_product_id):
    shop_product = ShopProduct.objects.get(id=shop_product_id)

    # All Shop Product in all Invoice Purchases
    sum_all_shop_p_numbers_invoice_purchases = PurchaseToShopProduct.objects.filter(
        shop_product=shop_product).aggregate(Sum('unit_numbers'))

    # All Shop Product in all Invoice return (Customer to Cafe)
    sum_all_shop_p_numbers_invoice_return_c_to_cafe = InvoiceReturn.objects.filter(
        shop_product=shop_product, return_type="CUSTOMER_TO_CAFE").aggregate(Sum('numbers'))

    # All Shop Products in Invoice return Cafe to Supplier
    sum_all_shop_p_numbers_invoice_return_cafe_to_s = InvoiceReturn.objects.filter(
        shop_product=shop_product, return_type="CAFE_TO_SUPPLIER").aggregate(Sum('numbers'))

    # All Shop Products in Amani Sales
    sum_all_shop_p_numbers_amani_sales = AmaniSale.objects.filter(
        invoice_sale_to_shop__shop_product=shop_product).aggregate(Sum('numbers'))

    if not sum_all_shop_p_numbers_invoice_purchases['unit_numbers__sum']:
        sum_all_shop_p_numbers_invoice_purchases['unit_numbers__sum'] = 0
    if not sum_all_shop_p_numbers_invoice_return_c_to_cafe['numbers__sum']:
        sum_all_shop_p_numbers_invoice_return_c_to_cafe['numbers__sum'] = 0
    if not sum_all_shop_p_numbers_invoice_return_cafe_to_s['numbers__sum']:
        sum_all_shop_p_numbers_invoice_return_cafe_to_s['numbers__sum'] = 0
    if not sum_all_shop_p_numbers_amani_sales['numbers__sum']:
        sum_all_shop_p_numbers_amani_sales['numbers__sum'] = 0

    real_shop_p_num = (sum_all_shop_p_numbers_invoice_purchases['unit_numbers__sum'] +
                       sum_all_shop_p_numbers_invoice_return_c_to_cafe[
                           'numbers__sum']) - (
                          sum_all_shop_p_numbers_invoice_return_cafe_to_s['numbers__sum'] +
                          sum_all_shop_p_numbers_amani_sales['numbers__sum'])

    return real_shop_p_num

class CreateNewInvoiceReturnView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_return_id = rec_data.get('id')

        if invoice_return_id == 0:
            supplier_id = rec_data.get('supplier_id')
            return_products = rec_data.get('return_products')
            return_type = rec_data.get('return_type')
            branch_id = rec_data.get('branch_id')
            invoice_date = rec_data.get('date')
            factor_number = rec_data.get('factor_number')
            banking_id = rec_data.get('banking_id')
            stock_id = rec_data.get('stock_id')

            if not branch_id or not return_products or not return_type or not invoice_date or not factor_number:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            branch_obj = Branch.objects.get(pk=branch_id)

            invoice_date_split = invoice_date.split('/')
            invoice_date_g = jdatetime.datetime(int(invoice_date_split[2]), int(invoice_date_split[1]),
                                                int(invoice_date_split[0]), datetime.now().hour, datetime.now().minute,
                                                datetime.now().second).togregorian()

            if banking_id:
                try:
                    banking_obj = BankingBaseClass.objects.get(pk=banking_id)
                except:
                    return JsonResponse({"error_msg": BANKING_NOT_FOUND}, status=404)
            else:
                banking_obj = None

            if stock_id:
                try:
                    stock_obj = Stock.objects.get(pk=stock_id)
                except:
                    return JsonResponse({"error_msg": STOCK_NOT_FOUND}, status=404)
            else:
                stock_obj = None

            last_invoice_obj = InvoiceReturn.objects.filter(branch=branch_obj).order_by('id').last()
            if last_invoice_obj:
                new_factor_number = last_invoice_obj.factor_number + 1
            else:
                new_factor_number = 1
            if new_factor_number != factor_number:
                return JsonResponse({"response_code": 3, "error_msg": FACTOR_NUMBER_INVALID})

            for return_product in return_products:
                shop_id = return_product['shop_id']
                numbers = return_product['numbers']
                description = return_product['description']
                shop_obj = ShopProduct.objects.get(pk=shop_id)
                if not shop_id:
                    return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
                if not numbers:
                    return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
                if not description:
                    return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

                if return_type == "CUSTOMER_TO_CAFE":
                    return_number_count = int(numbers)
                    all_amani_sales = AmaniSale.objects.filter(invoice_sale_to_shop__shop_product=shop_obj).order_by(
                        '-created_date')
                    for amani_sale in all_amani_sales:
                        real_number_in_amani_sale = amani_sale.numbers - amani_sale.return_numbers
                        if return_number_count <= real_number_in_amani_sale:
                            return_number_count = 0
                            break
                        else:
                            return_number_count -= real_number_in_amani_sale
                    if return_number_count != 0:
                        return JsonResponse({"response_code": 3,
                                             "error_msg": f"{AMANI_SALE_FOR_RETURN_NOT_ENOUGH} ( {shop_obj.name} )"})

                elif return_type == "CAFE_TO_SUPPLIER":
                    shop_product_real_numbers = get_detail_product_number(shop_obj.id)
                    if shop_product_real_numbers < int(numbers):
                        return JsonResponse({"response_code": 3,
                                             "error_msg": f"{NOT_ENOUGH_IN_STOCK} ( {shop_obj.name} ({shop_product_real_numbers}) )"})

                    if not supplier_id:
                        return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})
                    supplier_obj = Supplier.objects.get(pk=supplier_id)

                    can_returned_nums = 0
                    all_purchase_to_shop_p = PurchaseToShopProduct.objects.filter(shop_product=shop_obj,
                                                                                  invoice_purchase__supplier=supplier_obj)
                    for purchase in all_purchase_to_shop_p:
                        can_returned_nums += purchase.unit_numbers - purchase.buy_numbers - purchase.return_numbers

                    if can_returned_nums < int(numbers):
                        return JsonResponse({"response_code": 3, "error_msg": NOT_ENOUGH_IN_SUPPLIER})

                shop_id = return_product['shop_id']
                description = return_product['description']
                numbers = return_product['numbers']
                shop_obj = ShopProduct.objects.get(pk=shop_id)
                new_invoice = InvoiceReturn(
                    branch=branch_obj,
                    created_time=invoice_date_g,
                    shop_product=shop_obj,
                    description=description,
                    numbers=numbers,
                    return_type=return_type,
                    factor_number=new_factor_number,
                    banking=banking_obj,
                    stock=stock_obj,
                )
                new_invoice.save()

                if return_type == "CUSTOMER_TO_CAFE":
                    return_number_count = int(numbers)
                    all_amani_sales = AmaniSale.objects.filter(invoice_sale_to_shop__shop_product=shop_obj).order_by(
                        '-created_date')
                    for amani_sale in all_amani_sales:
                        real_number_in_amani_sale = amani_sale.numbers - amani_sale.return_numbers
                        if return_number_count <= real_number_in_amani_sale:
                            amani_sale.return_numbers += return_number_count
                            amani_sale.save()
                            new_amani_to_return = AmaniSaleToInvoiceReturn(
                                amani_sale=amani_sale,
                                invoice_return=new_invoice,
                                numbers=return_number_count
                            )
                            new_amani_to_return.save()
                            new_invoice.total_price += amani_sale.buy_price * return_number_count
                            new_invoice.save()
                            amani_to_purchase = AmaniSaleToInvoicePurchaseShopProduct.objects.filter(
                                amani_sale=amani_sale)
                            if amani_to_purchase:
                                amani_to_purchase[0].invoice_purchase_to_shop_product.buy_numbers -= return_number_count
                                amani_to_purchase[0].invoice_purchase_to_shop_product.save()
                            else:
                                return JsonResponse(
                                    {"response_code": 3, "error_msg": THE_INVOICE_PURCHASE_FOR_INVOICE_RETURN_NOT_FOUND})
                            break
                        else:
                            amani_sale.return_numbers += real_number_in_amani_sale
                            new_amani_to_return = AmaniSaleToInvoiceReturn(
                                amani_sale=amani_sale,
                                invoice_return=new_invoice,
                                numbers=real_number_in_amani_sale
                            )
                            new_amani_to_return.save()
                            new_invoice.total_price += amani_sale.buy_price * real_number_in_amani_sale
                            new_invoice.save()
                            amani_to_purchase = AmaniSaleToInvoicePurchaseShopProduct.objects.filter(
                                amani_sale=amani_sale)
                            if amani_to_purchase:
                                amani_to_purchase[
                                    0].invoice_purchase_to_shop_product.buy_numbers -= real_number_in_amani_sale
                                amani_to_purchase[0].invoice_purchase_to_shop_product.save()
                            else:
                                return JsonResponse(
                                    {"response_code": 3, "error_msg": THE_INVOICE_PURCHASE_FOR_INVOICE_RETURN_NOT_FOUND})
                            return_number_count -= real_number_in_amani_sale
                            amani_sale.save()

                elif return_type == 'CAFE_TO_SUPPLIER':
                    want_to_return = int(numbers)

                    new_invoice.supplier = supplier_obj
                    new_invoice.save()

                    for purchase in all_purchase_to_shop_p:
                        can_return_num_in_purchase = purchase.unit_numbers - purchase.buy_numbers - purchase.return_numbers
                        if want_to_return <= can_return_num_in_purchase != 0:
                            purchase.return_numbers += want_to_return
                            purchase.save()
                            new_return_to_purchase = PurchaseToInvoiceReturn(
                                invoice_return=new_invoice,
                                invoice_purchase_to_shop_product=purchase,
                                numbers=want_to_return
                            )
                            new_return_to_purchase.save()
                            new_invoice.total_price += want_to_return * purchase.base_unit_price
                            new_invoice.save()
                            break
                        else:
                            purchase.return_numbers += can_return_num_in_purchase
                            purchase.save()
                            new_return_to_purchase = PurchaseToInvoiceReturn(
                                invoice_return=new_invoice,
                                invoice_purchase_to_shop_product=purchase,
                                numbers=can_return_num_in_purchase
                            )
                            new_return_to_purchase.save()
                            new_invoice.total_price += can_return_num_in_purchase * purchase.base_unit_price
                            new_invoice.save()
                            want_to_return -= can_return_num_in_purchase

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 3, "error_msg": "Wrong ID!"})


class GetAllInvoicesReturnView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data.get('branch_id')

        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        invoice_objects = InvoiceReturn.objects.filter(branch=branch_obj).order_by('-id')[:100]
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)

            if invoice.supplier:
                supplier_name = invoice.supplier.name
            else:
                supplier_name = ""
            invoices.append({
                'id': invoice.pk,
                'factor_number': invoice.factor_number,
                'supplier_name': supplier_name,
                'shop_name': invoice.shop_product.name,
                'numbers': invoice.numbers,
                'total_price': invoice.total_price,
                'description': invoice.description,
                'date': jalali_date.strftime("%Y/%m/%d")
            })

        return JsonResponse({"response_code": 2, 'invoices': invoices})


class SearchInvoicesReturnView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS,
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data.get('search_word')

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
                'numbers': invoice_return.numbers,
                'total_price': invoice_return.total_price,
                'description': invoice_return.description,
                'date': jalali_date.strftime("%Y/%m/%d")
            })
        return JsonResponse({"response_code": 2, 'returns': returns})


class DeleteInvoicesReturnView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS,
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data['invoice_id']

        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        invoice_obj = InvoicePurchase.objects.get(pk=invoice_id)
        invoice_type = invoice_obj.settlement_type

        if invoice_type == "CASH":
            invoice_obj.delete()

        elif invoice_type == "CREDIT":
            invoice_obj.delete()

        return JsonResponse({"response_code": 2})
