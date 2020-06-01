from django.http import JsonResponse
import json
from django.db import IntegrityError
from accounti.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from accountiboard.constants import *


def login(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        password = rec_data['password']
        if not username:
            return JsonResponse({"response_code": 3, "error_msg": USERNAME_ERROR})

        if not password:
            return JsonResponse({"response_code": 3, "error_msg": PASSWORD_ERROR})

        try:
            user_obj = User.objects.get(phone=username)
            user_pass = user_obj.password
            if check_password(password, user_pass):
                user_obj.last_login = datetime.now()
                user_obj.save()
                if user_obj.get_user_type_display() == "cafe_owner":
                    cafe_owner_object = CafeOwner.objects.get(user=user_obj)
                    organization_object = cafe_owner_object.organization
                    branch_object = Branch.objects.filter(organization=organization_object).first()
                    request.session['user_role'] = USER_ROLES['CAFE_OWNER']
                elif user_obj.get_user_type_display() == "employee":
                    employee_object = Employee.objects.get(user=user_obj)
                    print(employee_object.employee_roles)
                    request.session['user_role'] = employee_object.employee_roles
                    branch_object = EmployeeToBranch.objects.get(employee=Employee.objects.get(user=user_obj)).branch
                else:
                    return JsonResponse({"response_code": 3})

                request.session['is_logged_in'] = username
                return JsonResponse(
                    {"response_code": 2,
                     "user_data": {'username': username, 'branch': branch_object.pk}})
            else:
                return JsonResponse({"response_code": 3, "error_msg": WRONG_USERNAME_OR_PASS})
        except ObjectDoesNotExist:
            return JsonResponse({"response_code": 3, "error_msg": WRONG_USERNAME_OR_PASS})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def register_employee(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    employee_id = rec_data['employee_id']
    first_name = rec_data['first_name']
    last_name = rec_data['last_name']
    father_name = rec_data['father_name']
    national_code = rec_data['national_code']
    phone = rec_data['phone']
    password = rec_data['password']
    re_password = rec_data['re_password']
    home_address = rec_data['home_address']
    bank_name = rec_data['bank_name']
    bank_card_number = rec_data['bank_card_number']
    shaba = rec_data['shaba']
    position = rec_data['position']
    auth_level = rec_data['auth_level']
    branch_id = rec_data['branch_id']

    if not phone:
        return JsonResponse({"response_code": 3, "error_msg": PHONE_ERROR})

    if not password and employee_id == '':
        return JsonResponse({"response_code": 3, "error_msg": PASSWORD_ERROR})

    if password != re_password:
        return JsonResponse({"response_code": 3, "error_msg": NOT_SIMILAR_PASSWORD})

    if not first_name:
        return JsonResponse({"response_code": 3, "error_msg": FIRST_NAME_REQUIRED})

    if not last_name:
        return JsonResponse({"response_code": 3, "error_msg": LAST_NAME_REQUIRED})

    if not father_name:
        return JsonResponse({"response_code": 3, "error_msg": FATHER_NAME_REQUIRED})

    if not national_code:
        return JsonResponse({"response_code": 3, "error_msg": NATIONAL_ID_REQUIRED})

    if not home_address:
        return JsonResponse({"response_code": 3, "error_msg": ADDRESS_REQUIRED})

    if not bank_name:
        return JsonResponse({"response_code": 3, "error_msg": BANK_NAME_REQUIRED})

    if not bank_card_number:
        return JsonResponse({"response_code": 3, "error_msg": CREDIT_CARD_REQUIRED})

    if not shaba:
        return JsonResponse({"response_code": 3, "error_msg": SHABA_REQUIRED})

    if not position:
        return JsonResponse({"response_code": 3, "error_msg": POSITION_REQUIRED})

    if auth_level == "":
        return JsonResponse({"response_code": 3, "error_msg": AUTH_LEVEL_REQUIRED})

    if not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": BRANCH_REQUIRED})

    if employee_id == 0:
        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=phone + "@gmail.com",
                password=make_password(password),
                home_address=home_address,
                user_type=USER_TYPE['employee']
            )
            new_user.save()
        except IntegrityError:
            return JsonResponse({"response_code": 3, "error_msg": PHONE_ALREADY_EXIST})

        new_employee = Employee(
            father_name=father_name,
            national_code=national_code,
            bank_name=bank_name,
            bank_card_number=bank_card_number,
            shaba_number=shaba,
            user=new_user
        )
        new_employee.save()
        new_employee_to_branch = EmployeeToBranch(
            branch=Branch.objects.get(pk=branch_id),
            employee=new_employee,
            position=position,
            auth_level=int(auth_level)
        )
        new_employee_to_branch.save()
        return JsonResponse({"response_code": 2})
    else:
        old_employee = Employee.objects.get(pk=employee_id)
        old_employee_to_branch = EmployeeToBranch.objects.get(employee=old_employee)
        old_employee.user.first_name = first_name
        old_employee.user.last_name = last_name
        old_employee.user.phone = phone
        old_employee.father_name = father_name
        old_employee.national_code = national_code
        if password != '' and re_password != '':
            if password == re_password:
                old_employee.user.password = make_password(password)
            else:
                return JsonResponse({"response_code": 3, "error_msg": NOT_SIMILAR_PASSWORD})
        old_employee.user.home_address = home_address
        old_employee.bank_name = bank_name
        old_employee.bank_card_number = bank_card_number
        old_employee.shaba_number = shaba

        old_employee.user.save()
        old_employee.save()

        old_employee_to_branch.position = position
        old_employee_to_branch.auth_level = int(auth_level)
        old_employee_to_branch.save()
        return JsonResponse({"response_code": 2})


def search_employee(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    search_word = rec_data['search_word']
    branch_id = rec_data['branch_id']
    if not search_word:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    employees_from_branch = EmployeeToBranch.objects.filter(branch=Branch.objects.get(pk=branch_id))
    employees = []
    for employee in employees_from_branch:
        if search_word in employee.employee.last_name:
            employees.append({
                "last_name": employee.employee.last_name,
                "position": employee.position,
                "auth_lvl": employee.auth_level,
            })
    return JsonResponse({"response_code": 2, 'employees': employees})


def check_login(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    if request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 2})
    else:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})


def log_out(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    if request.session.get('is_logged_in', None) == username:
        request.session['is_logged_in'] = {}
        return JsonResponse({"response_code": 2})
    else:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})


def get_employees(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    else:
        branch_id = rec_data['branch']
        organization_object = Branch.objects.get(id=branch_id).organization
        all_organization_branches = Branch.objects.filter(organization=organization_object)
        all_employees = EmployeeToBranch.objects.filter(branch__in=all_organization_branches)
        employees = []
        for employee in all_employees:
            employees.append({
                "id": employee.employee.pk,
                "last_name": employee.employee.user.last_name,
                "position": employee.position,
                "auth_lvl": employee.auth_level,
            })
        return JsonResponse({"response_code": 2, 'employees': employees})


def get_employee(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    else:
        employee_id = rec_data['employee_id']
        employee = Employee.objects.get(pk=employee_id)
        employee_to_branch = EmployeeToBranch.objects.get(employee=employee)
        employee_data = {
            'first_name': employee.user.first_name,
            'last_name': employee.user.last_name,
            'father_name': employee.father_name,
            'national_code': employee.national_code,
            'phone': employee.user.phone,
            'home_address': employee.user.home_address,
            'bank_name': employee.bank_name,
            'bank_card_number': employee.bank_card_number,
            'shaba': employee.shaba_number,
            'position': employee_to_branch.position,
            'auth_level': employee_to_branch.auth_level,
        }
        return JsonResponse({"response_code": 2, 'employee': employee_data})


def get_menu_categories(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    else:
        all_menu_categories = MenuCategory.objects.filter(branch_id=branch_id).order_by('list_order')
        menu_categories = []
        for category in all_menu_categories:
            menu_categories.append({
                "id": category.pk,
                "name": category.name,
            })
        return JsonResponse({"response_code": 2, 'menu_categories': menu_categories})


def get_menu_category(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')
    menu_category_id = rec_data.get('menu_category_id')

    if not branch_id or not menu_category_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    menu_category = MenuCategory.objects.get(pk=menu_category_id)
    all_cat_to_printer = PrinterToCategory.objects.filter(menu_category=menu_category)

    printers = Printer.objects.filter(branch_id=branch_id)
    printers_data = []
    for printer in printers:
        printers_data.append({
            'printer_id': printer.pk,
            'printer_name': printer.name,
            'is_checked': 0
        })

    printers_id = []
    for printer in all_cat_to_printer:
        printers_id.append(printer.printer.pk)
        for element in printers_data:
            if element['printer_id'] == printer.printer.pk:
                element['is_checked'] = 1
                break
    menu_category_data = {
        'id': menu_category.pk,
        'name': menu_category.name,
        'kind': menu_category.kind,
        'printers_id': printers_id,
        'printers': printers_data,
    }
    return JsonResponse({"response_code": 2, 'menu_category': menu_category_data})


def add_menu_category(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    menu_category_id = rec_data['menu_category_id']
    name = rec_data['name']
    kind = rec_data['kind']
    printers_id = rec_data['printers_id']
    username = rec_data['username']
    branch_id = rec_data['branch_id']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not name or not kind or not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    if menu_category_id == 0:
        new_menu_category = MenuCategory(name=name, kind=kind, branch_id=branch_id)
        new_menu_category.save()
        for printer_id in printers_id:
            printer_object = Printer.objects.get(pk=printer_id)
            new_printer_to_menu_cat = PrinterToCategory(
                printer=printer_object,
                menu_category=new_menu_category
            )
            new_printer_to_menu_cat.save()
        return JsonResponse({"response_code": 2})
    else:
        old_menu_category = MenuCategory.objects.get(pk=menu_category_id)
        PrinterToCategory.objects.filter(menu_category=old_menu_category).delete()
        old_menu_category.name = name
        old_menu_category.kind = kind
        for printer_id in printers_id:
            printer_object = Printer.objects.get(pk=printer_id)
            PrinterToCategory(printer=printer_object, menu_category=old_menu_category).save()
        old_menu_category.save()
        return JsonResponse({"response_code": 2})


def search_menu_category(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        branch_id = rec_data['branch_id']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word or not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        categories_searched = MenuCategory.objects.filter(name__contains=search_word, branch_id=branch_id)
        menu_categories = []
        for category in categories_searched:
            menu_categories.append({
                "name": category.name,
            })
        return JsonResponse({"response_code": 2, 'menu_categories': menu_categories})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_menu_items(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    all_menu_items = MenuItem.objects.filter(is_delete=0, menu_category__branch_id=branch_id).order_by(
        'menu_category__name')
    menu_items = []
    for item in all_menu_items:
        menu_items.append({
            "id": item.pk,
            "name": item.name,
            "price": item.price,
            "category_name": item.menu_category.name,
            "menu_category_id": item.menu_category.id
        })
    return JsonResponse({"response_code": 2, 'menu_items': menu_items})


def get_menu_item(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            menu_item_id = rec_data['menu_item_id']
            menu_item = MenuItem.objects.get(pk=menu_item_id)
            menu_item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
                "category_name": menu_item.menu_category.name,
                "menu_category_id": menu_item.menu_category.id
            }
            return JsonResponse({"response_code": 2, 'menu_item': menu_item_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def add_menu_item(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    menu_item_id = rec_data['menu_item_id']
    menu_category_id = rec_data['menu_category_id']
    name = rec_data['name']
    price = rec_data['price']
    username = rec_data['username']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    if not name:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not price:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not menu_category_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    if menu_item_id == 0:
        new_menu_item = MenuItem(
            name=name,
            price=price,
            menu_category=MenuCategory.objects.get(pk=menu_category_id)
        )
        new_menu_item.save()
        return JsonResponse({"response_code": 2})
    else:
        old_menu_item = MenuItem.objects.get(pk=menu_item_id)
        old_menu_item.name = name
        old_menu_item.price = price
        old_menu_item.menu_category = MenuCategory.objects.get(pk=menu_category_id)
        old_menu_item.save()
        return JsonResponse({"response_code": 2})


def delete_menu_item(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        menu_item_id = rec_data['menu_item_id']
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        if not menu_item_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        old_menu_item = MenuItem.objects.get(pk=menu_item_id)
        old_menu_item.is_delete = 1
        old_menu_item.save()
        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_menu_item(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        branch_id = rec_data['branch_id']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = MenuItem.objects.filter(name__contains=search_word, is_delete=0,
                                                 menu_category__branch_id=branch_id)
        menu_items = []
        for item in items_searched:
            menu_items.append({
                "id": item.pk,
                "name": item.name,
                "price": item.price,
                "category_name": item.menu_category.name,
                "menu_category_id": item.menu_category.id
            })

        items_searched = MenuItem.objects.filter(menu_category__name__contains=search_word, is_delete=0)
        for item in items_searched:
            menu_items.append({
                "id": item.pk,
                "name": item.name,
                "price": item.price,
                "category_name": item.menu_category.name,
                "menu_category_id": item.menu_category.id
            })
        return JsonResponse({"response_code": 2, 'menu_items': menu_items})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_menu_items_with_categories(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        menu_items_with_categories_data = []
        menu_categories = MenuCategory.objects.filter(branch_id=branch_id).order_by('list_order')
        for cat in menu_categories:
            menu_items = MenuItem.objects.filter(menu_category=cat, is_delete=0)
            menu_items_data = []
            for item in menu_items:
                menu_items_data.append({
                    'id': item.pk,
                    'name': item.name,
                    'price': item.price
                })
            menu_items_with_categories_data.append({
                'category_name': cat.name,
                'items': menu_items_data,
            })
        return JsonResponse({"response_code": 2, 'menu_items_with_categories': menu_items_with_categories_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_printers(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')

    if not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    printers = Printer.objects.filter(branch_id=branch_id)
    printers_data = []
    for printer in printers:
        printers_data.append({
            'printer_id': printer.pk,
            'printer_name': printer.name,
            'is_checked': 0
        })
    return JsonResponse({"response_code": 2, 'printers': printers_data})


def get_today_cash(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        branch_obj = Branch.objects.get(pk=branch_id)
        cash_obj = Cash.objects.filter(branch=branch_obj, is_close=0)
        if len(cash_obj) == 1:
            return JsonResponse({"response_code": 2, 'cash_id': cash_obj[0].id})
        else:
            return JsonResponse({"response_code": 3, 'error_message': CASH_ERROR})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
