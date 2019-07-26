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


def get_invoice(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        invoice_id = rec_data['invoice_id']
        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        invoice_object = InvoicePurchase.objects.get(pk=invoice_id)
        invoice_data = {
            'id': invoice_object.pk,
            'supplier_id': invoice_object.supplier.id,
            'material_items': [],
            'shop_product_items': [],
            'total_price': invoice_object.total_price,
            'settlement_type': invoice_object.settlement_type,
            'tax': invoice_object.tax,
            'discount': invoice_object.discount,
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
            username = rec_data['username']
            branch_id = rec_data['branch_id']

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not request.session['is_logged_in'] == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
            if not branch_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if len(material_items) == 0 and len(shop_product_items) == 0:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if total_price == 0:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if supplier_id == 0:
                return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})

            branch_obj = Branch.objects.get(pk=branch_id)
            supplier_obj = Supplier.objects.get(pk=supplier_id)

            new_invoice = InvoicePurchase(
                branch=branch_obj,
                created_time=datetime.now(),
                supplier=supplier_obj,
                settlement_type=settlement_type,
                tax=tax,
                discount=discount,
                total_price=total_price
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
                item_obj.real_numbers += item['nums']
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

            if settlement_type == "CREDIT":
                supplier_obj.remainder += total_price
                supplier_obj.save()

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_all_invoices(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch_id']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        invoice_objects = InvoicePurchase.objects.filter(branch=branch_obj)
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            invoices.append({
                'id': invoice.pk,
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
        if not request.session['is_logged_in'] == username:
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
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        materials = Material.objects.all()
        materials_data = []
        for material in materials:
            materials_data.append({
                'id': material.pk,
                'name': material.name,
                'unit': material.unit
            })
        return JsonResponse({"response_code": 2, 'materials': materials_data})


def get_shop_products(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        shop_products = ShopProduct.objects.all()
        shop_products_data = []
        for shop in shop_products:
            shop_products_data.append({
                'id': shop.pk,
                'name': shop.name,
                'price': shop.price,
                'real_numbers': shop.real_numbers
            })
        return JsonResponse({"response_code": 2, 'shop_products': shop_products_data})


def get_last_buy_price(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        shop_product_id = rec_data['shop_product_id']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not shop_product_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        shop_product = ShopProduct.objects.get(pk=shop_product_id)
        last_invoice_purchase = PurchaseToShopProduct.objects.filter(shop_product=shop_product).last()

        return JsonResponse({"response_code": 2, 'last_buy_price': last_invoice_purchase.base_unit_price})


def search_materials(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Material.objects.filter(name__contains=search_word)
        materials = []
        for material in items_searched:
            materials.append({
                'id': material.pk,
                'name': material.name,
                'unit': material.unit
            })
        return JsonResponse({"response_code": 2, 'materials': materials})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_shop_products(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = ShopProduct.objects.filter(name__contains=search_word)
        shops = []
        for shop in items_searched:
            shops.append({
                'id': shop.pk,
                'name': shop.name,
                'price': shop.price,
                'real_numbers': shop.real_numbers
            })
        return JsonResponse({"response_code": 2, 'shop_products': shops})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def add_material(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        material_name = rec_data['material_name']
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not material_name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        new_material = Material(name=material_name)
        new_material.save()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def add_shop_product(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        shop_product_name = rec_data['shop_product_name']
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not shop_product_name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        new_shop_product = ShopProduct(name=shop_product_name)
        new_shop_product.save()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def delete_invoice_purchase(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data['invoice_id']
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        invoice_obj = InvoicePurchase.objects.get(pk=invoice_id)
        invoice_type = invoice_obj.settlement_type

        if invoice_type == "CASH":
            invoice_obj.delete()

        elif invoice_type == "AMANI":
            pass

        elif invoice_type == "CREDIT":
            invoice_obj.supplier.remainder -= invoice_obj.total_price
            invoice_obj.supplier.save()
            invoice_obj.delete()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

