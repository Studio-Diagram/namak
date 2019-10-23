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
FACTOR_NUMBER_INVALID = "شماره فاکتور تطابق ندارد."


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
            username = rec_data['username']
            branch_id = rec_data['branch_id']
            invoice_date = rec_data['date']
            factor_number = rec_data['factor_number']

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not request.session.get('is_logged_in', None) == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
            if not branch_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not shop_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not numbers:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not description:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not return_type:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not invoice_date:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not factor_number:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            branch_obj = Branch.objects.get(pk=branch_id)
            shop_obj = ShopProduct.objects.get(pk=shop_id)

            if shop_obj.real_numbers < int(numbers):
                return JsonResponse({"response_code": 3, "error_msg": "Not Enough in Stock!"})

            invoice_date_split = invoice_date.split('/')
            invoice_date_g = jdatetime.datetime(int(invoice_date_split[2]), int(invoice_date_split[1]),
                                                int(invoice_date_split[0]), datetime.now().hour, datetime.now().minute,
                                                datetime.now().second).togregorian()

            last_invoice_obj = InvoiceReturn.objects.filter(branch=branch_obj).order_by('id').last()
            if last_invoice_obj:
                new_factor_number = last_invoice_obj.factor_number + 1
            else:
                new_factor_number = 1
            if new_factor_number != factor_number:
                return JsonResponse({"response_code": 3, "error_msg": FACTOR_NUMBER_INVALID})

            new_invoice = InvoiceReturn(
                branch=branch_obj,
                created_time=invoice_date_g,
                shop_product=shop_obj,
                description=description,
                numbers=numbers,
                return_type=return_type,
                factor_number=new_factor_number
            )
            new_invoice.save()

            if return_type == "CUSTOMER_TO_CAFE":
                shop_obj.real_numbers += int(numbers)
                shop_obj.save()
                return_number_count = int(numbers)
                all_amani_sales = AmaniSale.objects.filter(invoice_sale_to_shop__shop_product=shop_obj).order_by(
                    '-created_date')
                for amani_sale in all_amani_sales:
                    real_number_in_amani_sale = amani_sale.numbers - amani_sale.return_numbers
                    if real_number_in_amani_sale != 0:
                        if return_number_count == real_number_in_amani_sale or return_number_count < real_number_in_amani_sale:
                            amani_sale.return_numbers += return_number_count
                            amani_sale.save()
                            amani_sale.supplier.remainder -= amani_sale.buy_price * return_number_count
                            amani_sale.supplier.save()
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
                                return JsonResponse({"response_code": 3, "error_msg": "HOLY S***!"})

                            return_number_count = 0
                            break
                        else:
                            amani_sale.return_numbers += real_number_in_amani_sale
                            amani_sale.supplier.remainder -= amani_sale.buy_price * real_number_in_amani_sale
                            amani_sale.supplier.save()
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
                                return JsonResponse({"response_code": 3, "error_msg": "HOLY S***!"})
                            return_number_count -= real_number_in_amani_sale
                            amani_sale.save()

            elif return_type == 'CAFE_TO_SUPPLIER':
                want_to_rerurn = int(numbers)
                if not supplier_id:
                    return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})
                supplier_obj = Supplier.objects.get(pk=supplier_id)
                new_invoice.supplier = supplier_obj
                new_invoice.save()

                can_returned_nums = 0
                all_purchase_to_shop_p = PurchaseToShopProduct.objects.filter(shop_product=shop_obj)
                for purchase in all_purchase_to_shop_p:
                    can_returned_nums += purchase.unit_numbers - purchase.buy_numbers - purchase.return_numbers

                if can_returned_nums < int(numbers):
                    return JsonResponse({"response_code": 3, "error_msg": "Not Enough in Supplier!"})

                shop_obj.real_numbers -= int(numbers)
                shop_obj.save()

                for purchase in all_purchase_to_shop_p:
                    can_return_num_in_purchase = purchase.unit_numbers - purchase.buy_numbers - purchase.return_numbers
                    if want_to_rerurn <= can_return_num_in_purchase != 0:
                        purchase.return_numbers += want_to_rerurn
                        purchase.save()
                        new_return_to_purchase = PurchaseToInvoiceReturn(
                            invoice_return=new_invoice,
                            invoice_purchase_to_shop_product=purchase,
                            numbers=want_to_rerurn
                        )
                        new_return_to_purchase.save()
                        new_invoice.total_price += want_to_rerurn * purchase.base_unit_price
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
                        want_to_rerurn -= can_return_num_in_purchase

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
                'numbers': invoice_return.numbers,
                'total_price': invoice_return.total_price,
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
