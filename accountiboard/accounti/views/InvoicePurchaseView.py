from django.http import JsonResponse
from accounti.models import *
from datetime import datetime
import jdatetime, json
from django.db.models import Sum
from accountiboard.constants import *


def get_invoice(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        invoice_id = rec_data['invoice_id']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        invoice_object = InvoicePurchase.objects.get(pk=invoice_id)
        invoice_date = invoice_object.created_time.date()
        jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                   year=invoice_date.year)

        try:
            banking_obj = BankingBaseClass.objects.get(pk=invoice_object.banking.id)
        except:
            banking_obj = None

        try:
            stock_obj = Stock.objects.get(pk=invoice_object.stock.id)
        except:
            stock_obj = None

        invoice_data = {
            'id': invoice_object.pk,
            'factor_number': invoice_object.factor_number,
            'supplier_id': invoice_object.supplier.id,
            'supplier_name': invoice_object.supplier.name,
            'material_items': [],
            'shop_product_items': [],
            'total_price': invoice_object.total_price,
            'settlement_type': invoice_object.settlement_type,
            'tax': invoice_object.tax,
            'discount': invoice_object.discount,
            'created_date': jalali_date.strftime("%Y/%m/%d"),
            'settlement_type_name': invoice_object.get_settlement_type_display(),
            'banking': {'id': banking_obj.id, 'name': banking_obj.name} if banking_obj else {'id': None},
            'stock': {'id': stock_obj.id, 'name': stock_obj.name} if stock_obj else {'id': None},
        }

        invoice_materials = PurchaseToMaterial.objects.filter(invoice_purchase=invoice_object)
        for item in invoice_materials:
            invoice_data['material_items'].append({
                'id': item.material.pk,
                'name': item.material.name,
                'price': item.base_unit_price,
                'nums': item.unit_numbers,
                'total': item.base_unit_price * item.unit_numbers,
                'description': item.description
            })

        invoice_shop_products = PurchaseToShopProduct.objects.filter(invoice_purchase=invoice_object)
        for item in invoice_shop_products:
            invoice_data['shop_product_items'].append({
                'id': item.shop_product.pk,
                'name': item.shop_product.name,
                'price': item.base_unit_price,
                'sale_price': item.sale_price,
                'nums': item.unit_numbers,
                'total': item.base_unit_price * item.unit_numbers,
                'description': item.description
            })
        return JsonResponse({"response_code": 2, "invoice": invoice_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def create_new_invoice_purchase(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_purchase_id = rec_data['id']

        if invoice_purchase_id == 0:
            supplier_id = rec_data['supplier_id']
            material_items = rec_data['material_items']
            shop_product_items = rec_data['shop_product_items']
            total_price = rec_data['total_price']
            settlement_type = rec_data['settlement_type']
            tax = rec_data['tax']
            discount = rec_data['discount']
            invoice_date = rec_data['date']
            factor_number = rec_data['factor_number']
            username = rec_data['username']
            branch_id = rec_data['branch_id']
            banking_id = rec_data.get('banking_id')
            stock_id = rec_data.get('stock_id')

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not request.session.get('is_logged_in', None) == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
            if not branch_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if len(material_items) == 0 and len(shop_product_items) == 0:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if total_price == 0:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if supplier_id == 0:
                return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})
            if not invoice_date:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not factor_number or tax == '' or discount == '':
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            if len(shop_product_items) and len(material_items):
                return JsonResponse({"response_code": 3, "error_msg": CAN_NOT_ADD_PURCHASE_MATERIAL_AND_SHOP_TOGETHER})

            branch_obj = Branch.objects.get(pk=branch_id)
            supplier_obj = Supplier.objects.get(pk=supplier_id)

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

            invoice_date_split = invoice_date.split('/')
            invoice_date_g = jdatetime.datetime(int(invoice_date_split[2]), int(invoice_date_split[1]),
                                                int(invoice_date_split[0]), datetime.now().hour, datetime.now().minute,
                                                datetime.now().second).togregorian()

            last_invoice_obj = InvoicePurchase.objects.filter(branch=branch_obj).order_by('id').last()
            if last_invoice_obj:
                new_factor_number = last_invoice_obj.factor_number + 1
            else:
                new_factor_number = 1
            if new_factor_number != factor_number:
                return JsonResponse({"response_code": 3, "error_msg": FACTOR_NUMBER_INVALID})

            new_invoice = InvoicePurchase(
                branch=branch_obj,
                created_time=invoice_date_g,
                supplier=supplier_obj,
                settlement_type=settlement_type,
                tax=tax,
                discount=discount,
                total_price=0,
                factor_number=new_factor_number,
                banking=banking_obj,
                stock=stock_obj,
            )
            new_invoice.save()

            for item in material_items:
                item_obj = Material.objects.get(pk=item['id'])
                new_item_to_invoice = PurchaseToMaterial(
                    invoice_purchase=new_invoice,
                    material=item_obj,
                    base_unit_price=item['price'],
                    unit_numbers=item['nums'],
                    description=item['description']
                )
                new_item_to_invoice.save()
                new_invoice.total_price += item['total']

            for item in shop_product_items:
                item_obj = ShopProduct.objects.get(pk=item['id'])
                item_obj.price = item['sale_price']
                item_obj.save()
                new_item_to_invoice = PurchaseToShopProduct(
                    invoice_purchase=new_invoice,
                    shop_product=item_obj,
                    base_unit_price=item['price'],
                    sale_price=item['sale_price'],
                    unit_numbers=item['nums'],
                    description=item['description']
                )
                new_item_to_invoice.save()
                new_invoice.total_price += item['total']

            new_invoice.total_price = int(new_invoice.total_price) + int(new_invoice.tax) - int(new_invoice.discount)

            new_invoice.save()

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 2})

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
        invoice_objects = InvoicePurchase.objects.filter(branch=branch_obj).order_by('-id')[:100]
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            invoices.append({
                'id': invoice.pk,
                'factor_number': invoice.factor_number,
                'supplier_id': invoice.supplier.pk,
                'supplier_name': invoice.supplier.name,
                'total_price': invoice.total_price,
                'kind': invoice.get_settlement_type_display(),
                'date': jalali_date.strftime("%Y/%m/%d")
            })

        return JsonResponse({"response_code": 2, 'invoices': invoices})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_all_invoice_games(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        invoice_id = rec_data['invoice_id']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        else:
            invoice_object = InvoiceSales.objects.get(pk=invoice_id)
            invoice_games = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_object)
            games = []
            for game in invoice_games:
                if str(game.game.end_time) != "00:00:00":
                    games.append({
                        'id': game.game.pk,
                        'numbers': game.game.numbers,
                        'start_time': game.game.start_time,
                        'end_time': game.game.end_time,
                        'points': game.game.points,
                        'total': game.game.points * 5000
                    })
            return JsonResponse({"response_code": 2, 'games': games})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_materials(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    organization_object = Branch.objects.get(id=branch_id).organization
    materials = Material.objects.filter(organization=organization_object)
    materials_data = []
    for material in materials:
        last_material_price = 0
        last_material = PurchaseToMaterial.objects.filter(material=material).last()
        if last_material:
            last_material_price = last_material.base_unit_price
        materials_data.append({
            'id': material.pk,
            'name': material.name,
            'unit': material.unit,
            'price': last_material_price
        })
    return JsonResponse({"response_code": 2, 'materials': materials_data})


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


def get_shop_products(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    shop_products = ShopProduct.objects.filter(branch_id=branch_id)
    shop_products_data = []
    for shop in shop_products:
        last_shop_price = 0
        last_shop = PurchaseToShopProduct.objects.filter(shop_product=shop).last()
        if last_shop:
            last_shop_price = last_shop.base_unit_price
        shop_products_data.append({
            'id': shop.pk,
            'name': shop.name,
            'price': shop.price,
            'buy_price': last_shop_price,
            'real_numbers': get_detail_product_number(shop.id)
        })
    shop_products_data = sorted(shop_products_data, key=lambda i: i['real_numbers'])
    shop_products_data.reverse()
    return JsonResponse({"response_code": 2, 'shop_products': shop_products_data})


def get_last_buy_price(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    shop_product_id = rec_data['shop_product_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not shop_product_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    shop_product = ShopProduct.objects.get(pk=shop_product_id)
    last_invoice_purchase = PurchaseToShopProduct.objects.filter(shop_product=shop_product).last()
    if last_invoice_purchase:
        last_price = last_invoice_purchase.base_unit_price
    else:
        last_price = 0

    return JsonResponse({"response_code": 2, 'last_buy_price': last_price})


def search_materials(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Material.objects.filter(name__contains=search_word)
        materials = []
        for material in items_searched:
            last_material_price = 0
            last_material = PurchaseToMaterial.objects.filter(material=material).last()
            if last_material:
                last_material_price = last_material.base_unit_price
            materials.append({
                'id': material.pk,
                'name': material.name,
                'unit': material.unit,
                'price': last_material_price
            })
        return JsonResponse({"response_code": 2, 'materials': materials})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_shop_products(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    search_word = rec_data.get('search_word')
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not search_word or not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    items_searched = ShopProduct.objects.filter(name__icontains=search_word, branch_id=branch_id)
    shops = []
    for shop in items_searched:
        last_shop_price = 0
        last_shop = PurchaseToShopProduct.objects.filter(shop_product=shop).last()
        if last_shop:
            last_shop_price = last_shop.base_unit_price
        shops.append({
            'id': shop.pk,
            'name': shop.name,
            'price': shop.price,
            'buy_price': last_shop_price,
            'real_numbers': get_detail_product_number(shop.id)
        })
    return JsonResponse({"response_code": 2, 'shop_products': shops})


def add_material(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    material_name = rec_data.get('material_name')
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not material_name or not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    organization_object = Branch.objects.get(id=branch_id).organization
    new_material = Material(name=material_name, organization=organization_object)
    new_material.save()

    return JsonResponse(
        {"response_code": 2, "new_material": {"id": new_material.pk, "name": new_material.name, "price": ZERO_PRICE}})


def add_shop_product(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    shop_product_name = rec_data.get('shop_product_name')
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not shop_product_name or not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    new_shop_product = ShopProduct(name=shop_product_name, branch_id=branch_id)
    new_shop_product.save()

    return JsonResponse({"response_code": 2,
                         "new_shop_product": {"id": new_shop_product.pk, "name": new_shop_product.name,
                                              "sale_price": ZERO_PRICE,
                                              "buy_price": ZERO_PRICE}})


def delete_invoice_purchase(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
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

    elif invoice_type == "AMANi":
        return JsonResponse({"response_code": 3, "error_msg": CAN_NOT_DELETE_PURCHASE_BECAUSE_AMANI})

    elif invoice_type == "CREDIT":
        if PurchaseToShopProduct.objects.filter(invoice_purchase=invoice_obj).count():
            return JsonResponse({"response_code": 3, "error_msg": CAN_NOT_DELETE_PURCHASE_BECAUSE_SHOP_PRODUCT})
        invoice_obj.delete()

    return JsonResponse({"response_code": 2})
