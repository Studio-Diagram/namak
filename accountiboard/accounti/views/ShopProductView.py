from django.http import JsonResponse
import json, jdatetime, datetime, xlwt
from accounti.models import *
from django.db.models import Sum
from accountiboard import settings
from accountiboard.constants import *


def get_detail_product_number(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "POST REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    shop_product_name = rec_data['shop_product_name']

    if not shop_product_name:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    shop_product = ShopProduct.objects.get(name=shop_product_name)

    # All Invoice Sales with this product
    invoice_sales_counter = InvoicesSalesToShopProducts.objects.filter(shop_product=shop_product).aggregate(Sum('numbers'))

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

    return JsonResponse({"response_code": 2, "num": real_shop_p_num,
                         "sum_all_shop_p_numbers_invoice_purchases": sum_all_shop_p_numbers_invoice_purchases,
                         "sum_all_shop_p_numbers_invoice_return_c_to_cafe": sum_all_shop_p_numbers_invoice_return_c_to_cafe,
                         "sum_all_shop_p_numbers_invoice_return_cafe_to_s": sum_all_shop_p_numbers_invoice_return_cafe_to_s,
                         "sum_all_shop_p_numbers_amani_sales": sum_all_shop_p_numbers_amani_sales,
                         "sum_all_invoice_sales_to_shop_product": invoice_sales_counter})
