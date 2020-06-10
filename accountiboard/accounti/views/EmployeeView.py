from django.http import JsonResponse
import json
from django.db import IntegrityError
from accounti.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from accountiboard.constants import *
from accountiboard.utils import make_new_JWT_token, decode_JWT_return_user
from accounti.validators.EmployeeValidator import *
from accountiboard.custom_permissions import *


def login(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    rec_data = json.loads(request.read().decode('utf-8'))

    validator = LoginValidator(rec_data)
    if not validator.is_valid():
        return JsonResponse({"response_code": 3, "error_msg": validator.errors})

    username = rec_data['username']
    password = rec_data['password']

    try:
        user_obj = User.objects.get(phone=username)
    except ObjectDoesNotExist:
        return JsonResponse({"response_code": 3, "error_msg": WRONG_USERNAME_OR_PASS})

    if not check_password(password, user_obj.password):
        return JsonResponse({"response_code": 3, "error_msg": WRONG_USERNAME_OR_PASS})

    user_obj.last_login = datetime.now()
    user_obj.save()
    if user_obj.get_user_type_display() == "cafe_owner":
        cafe_owner_object = CafeOwner.objects.get(user=user_obj)
        organization_object = cafe_owner_object.organization
        branch_object = Branch.objects.filter(organization=organization_object).first()
        user_branche_objects = Branch.objects.filter(organization=organization_object)
        user_branches = [{
            "id": cafe_owner_to_branch.id,
            "name": cafe_owner_to_branch.name
        } for cafe_owner_to_branch in user_branche_objects]
        user_role = USER_ROLES['CAFE_OWNER']
        request.session['user_role'] = [USER_ROLES['CAFE_OWNER']]
    elif user_obj.get_user_type_display() == "employee":
        employee_object = Employee.objects.get(user=user_obj)
        request.session['user_role'] = employee_object.employee_roles
        user_role = employee_object.employee_roles
        branches = EmployeeToBranch.objects.filter(employee=employee_object)
        branch_object = branches.first().branch.id
        user_branches = [{
            "id": employee_to_branch.branch.id,
            "name": employee_to_branch.branch.name,
        } for employee_to_branch in branches]
        request.session['is_logged_in'] = username
    else:
        return JsonResponse({"response_code": 3})

    jwt_token = make_new_JWT_token(user_obj.id, user_obj.phone, user_role, user_branches)
    return JsonResponse(
        {"response_code": 2,
         "user_data": {'username': username, 'branch': branch_object, 'branches': user_branches,
                       'user_roles': user_role},
         "token": jwt_token.decode("utf-8")
         }
    )


def register_employee(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    validator = RegisterEmployeeValidator(rec_data)
    if not validator.is_valid():
        return JsonResponse({"response_code": 3, "error_msg": validator.errors})

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
    auth_levels = rec_data['auth_levels']
    employee_branches = rec_data['employee_branches']

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
            user=new_user,
            employee_roles=[auth_level.get('id') for auth_level in auth_levels if
                            auth_level.get('is_checked') == 1]
        )
        new_employee.save()
        for employee_branch in employee_branches:
            new_employee_to_branch = EmployeeToBranch(
                branch=Branch.objects.get(pk=employee_branch.get('id')),
                employee=new_employee,
                position=DEFAULT_POSITTION  # TODO: Remove posittion from models
            )
            new_employee_to_branch.save()
        return JsonResponse({"response_code": 2})
    else:
        old_employee = Employee.objects.get(pk=employee_id)
        EmployeeToBranch.objects.filter(employee=old_employee).delete()
        old_employee.user.first_name = first_name
        old_employee.user.last_name = last_name
        old_employee.user.phone = phone
        old_employee.father_name = father_name
        old_employee.national_code = national_code
        old_employee.employee_roles = [auth_level.get('id') for auth_level in auth_levels if
                                       auth_level.get('is_checked') == 1]
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

        #  TODO: Needs to improve this section
        for employee_branch in employee_branches:
            if employee_branch.get('is_checked'):
                new_employee_to_branch = EmployeeToBranch(
                    branch=Branch.objects.get(pk=employee_branch.get('id')),
                    employee=old_employee,
                    position=DEFAULT_POSITTION  # TODO: Remove posittion from models
                )
                new_employee_to_branch.save()

        return JsonResponse({"response_code": 2})


def search_employee(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    rec_data = json.loads(request.read().decode('utf-8'))
    validator = SearchEmployeeValidator(rec_data)
    if not validator.is_valid():
        return JsonResponse({"response_code": 3, "error_msg": validator.errors})

    search_word = rec_data['search_word']
    branch_id = rec_data['branch_id']

    employees_from_branch = EmployeeToBranch.objects.filter(branch=Branch.objects.get(pk=branch_id))
    employees = []
    for employee in employees_from_branch:
        if search_word in employee.employee.last_name:
            employees.append({
                "last_name": employee.employee.last_name,
                "auth_lvl": employee.auth_level,
            })
    return JsonResponse({"response_code": 2, 'employees': employees})


@permission_decorator(token_authenticate, {USER_ROLES['CAFE_OWNER']})
def get_employees(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    rec_data = json.loads(request.read().decode('utf-8'))
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])

    branch_id = rec_data['branch']
    organization_object = Branch.objects.get(id=branch_id).organization
    all_organization_branches = Branch.objects.filter(organization=organization_object)
    all_employees = EmployeeToBranch.objects.filter(branch__in=all_organization_branches).values('employee').distinct()
    employees = []
    for employee in all_employees:
        employee_object = Employee.objects.get(id=employee.get('employee'))
        employee_branches = EmployeeToBranch.objects.filter(employee=employee_object)
        employees.append({
            "id": employee_object.pk,
            "full_name": employee_object.user.get_full_name(),
            "auth_levels": employee_object.employee_roles,
            "branches": [{
                "id": employee_branch.branch.id,
                "name": employee_branch.branch.name
            }for employee_branch in employee_branches],
        })
    return JsonResponse({"response_code": 2, 'employees': employees})


def get_employee(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    rec_data = json.loads(request.read().decode('utf-8'))
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    if not payload:
        # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
    employee_id = rec_data['employee_id']
    employee = Employee.objects.get(pk=employee_id)
    employee_to_branches = EmployeeToBranch.objects.filter(employee=employee)
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
        'auth_levels': employee.employee_roles,
        'branches': [employee_branch.branch.id for employee_branch in employee_to_branches]
    }
    return JsonResponse({"response_code": 2, 'employee': employee_data})


def get_menu_categories(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    rec_data = json.loads(request.read().decode('utf-8'))
    branch_id = rec_data['branch']
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    if not payload:
        # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
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
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    branch_id = rec_data.get('branch')
    menu_category_id = rec_data.get('menu_category_id')

    if not branch_id or not menu_category_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    if not payload:
        # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})

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
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    validator = AddMenuCategoryValidator(rec_data)
    if not validator.is_valid():
        return JsonResponse({"response_code": 3, "error_msg": validator.errors})

    menu_category_id = rec_data['menu_category_id']
    name = rec_data['name']
    kind = rec_data['kind']
    printers_id = rec_data['printers_id']
    branch_id = rec_data['branch_id']

    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    if not payload:
        # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
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
        validator = SearchEmployeeValidator(rec_data)
        if not validator.is_valid():
            return JsonResponse({"response_code": 3, "error_msg": validator.errors})

        search_word = rec_data['search_word']
        branch_id = rec_data['branch_id']
        payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
        if not payload:
            # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
            return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
        if not search_word or not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        categories_searched = MenuCategory.objects.filter(name__contains=search_word, branch_id=branch_id)
        menu_categories = []
        for category in categories_searched:
            menu_categories.append({
                "name": category.name,
            })
        return JsonResponse({"response_code": 2, 'menu_categories': menu_categories})
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


def get_menu_items(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    rec_data = json.loads(request.read().decode('utf-8'))
    branch_id = rec_data['branch']
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    if not payload:
        # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})

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
        payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
        if not payload:
            # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
            return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
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
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


def add_menu_item(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    validator = AddMenuItemValidator(rec_data)
    if not validator.is_valid():
        return JsonResponse({"response_code": 3, "error_msg": validator.errors})

    menu_item_id = rec_data['menu_item_id']
    menu_category_id = rec_data['menu_category_id']
    name = rec_data['name']
    price = rec_data['price']
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    if not payload:
        # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})

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
        payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
        if not payload:
            # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
            return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})

        if not menu_item_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        old_menu_item = MenuItem.objects.get(pk=menu_item_id)
        old_menu_item.is_delete = 1
        old_menu_item.save()
        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


def search_menu_item(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        validator = SearchEmployeeValidator(rec_data)
        if not validator.is_valid():
            return JsonResponse({"response_code": 3, "error_msg": validator.errors})

        search_word = rec_data['search_word']
        branch_id = rec_data['branch_id']
        payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
        if not payload:
            # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
            return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})

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
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


def get_menu_items_with_categories(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch']
        payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
        if not payload:
            # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
            return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
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
    return JsonResponse({"response_code": 4, "error_msg": "This endpoint only supports POST method."})


def get_printers(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "This endpoint only supports POST method."})
    rec_data = json.loads(request.read().decode('utf-8'))
    branch_id = rec_data.get('branch')

    if not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
    if not payload:
        # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})

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
        branch_id = rec_data['branch']
        payload = decode_JWT_return_user(request.META['HTTP_AUTHORIZATION'])
        if not payload:
            # PERFORM OTHER CHECKS, PERMISSIONS, BRANCH, ORGANIZATION, ETC
            return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})

        branch_obj = Branch.objects.get(pk=branch_id)
        cash_obj = Cash.objects.filter(branch=branch_obj, is_close=0)
        if len(cash_obj) == 1:
            return JsonResponse({"response_code": 2, 'cash_id': cash_obj[0].id})
        else:
            return JsonResponse({"response_code": 3, 'error_message': CASH_ERROR})
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
