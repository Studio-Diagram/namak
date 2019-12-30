from django.http import JsonResponse
import json
from accounti.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
PHONE_ERROR = 'شماره تلفن خود را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'
CASH_ERROR = "خطای صندوق"
FIRST_NAME_REQUIRED = 'نام را وارد کنید.'
LAST_NAME_REQUIRED = 'نام خانوادگی را وارد کنید.'
FATHER_NAME_REQUIRED = 'نام پدر را وارد کنید.'
NATIONAL_ID_REQUIRED = 'شماره شناسنامه را وارد کنید.'
ADDRESS_REQUIRED = 'آدرس را وارد کنید.'
BANK_NAME_REQUIRED = 'نام بانک را وارد کنید.'
CREDIT_CARD_REQUIRED = 'شماره کارت اعتباری را وارد کنید.'
SHABA_REQUIRED = 'شماره شبا را وارد کنید.'
POSITION_REQUIRED = 'سمت را وارد کنید.'
SHIFT_SALARY_REQUIRED = 'حقوق شیفت پایه را وارد کنید.'
SHIFT_NUMBER_REQUIRED = 'تعداد شیفت پایه را وارد کنید.'
AUTH_LEVEL_REQUIRED = 'سطح دسترسی را وارد کنید.'
MEMBER_CARD_REQUIRED = 'شماره کارت عضویت را وارد کنید.'
BRANCH_REQUIRED = 'شعبه وارد نشده است.'


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
            employee_obj = Employee.objects.get(phone=username)
            user_pass = employee_obj.password
            if check_password(password, user_pass):
                employee_obj.last_login = datetime.now()
                employee_obj.save()
                employee_to_branch_obj = EmployeeToBranch.objects.get(employee=employee_obj)
                request.session['is_logged_in'] = username
                return JsonResponse(
                    {"response_code": 2,
                     "user_data": {'username': username, 'branch': employee_to_branch_obj.branch.pk}})
            else:
                return JsonResponse({"response_code": 3, "error_msg": WRONG_USERNAME_OR_PASS})
        except ObjectDoesNotExist:
            return JsonResponse({"response_code": 3, "error_msg": WRONG_USERNAME_OR_PASS})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def register_employee(request):
    if request.method == "POST":
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
        membership_card_number = rec_data['membership_card_number']
        base_worksheet_salary = rec_data['base_worksheet_salary']
        base_worksheet_count = rec_data['base_worksheet_count']
        auth_level = rec_data['auth_level']
        branch_id = rec_data['branch_id']

        if not phone:
            return JsonResponse({"response_code": 3, "error_msg": PHONE_ERROR})

        if not password and employee_id == '':
            return JsonResponse({"response_code": 3, "error_msg": PASSWORD_ERROR})

        if password != re_password:
            return JsonResponse({"response_code": 3, "error_msg": NOT_SIMILAR_PASSWORD})

        if not base_worksheet_salary:
            return JsonResponse({"response_code": 3, "error_msg": SHIFT_SALARY_REQUIRED})

        if not base_worksheet_count:
            return JsonResponse({"response_code": 3, "error_msg": SHIFT_NUMBER_REQUIRED})

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

        if not membership_card_number:
            return JsonResponse({"response_code": 3, "error_msg": MEMBER_CARD_REQUIRED})

        if auth_level == "":
            return JsonResponse({"response_code": 3, "error_msg": AUTH_LEVEL_REQUIRED})

        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": BRANCH_REQUIRED})

        membership_card_number = membership_card_number.replace("؟", "")
        membership_card_number = membership_card_number.replace("٪", "")
        membership_card_number = membership_card_number.replace("?", "")
        membership_card_number = membership_card_number.replace("%", "")

        if employee_id == 0:
            new_employee = Employee(
                first_name=first_name,
                last_name=last_name,
                father_name=father_name,
                national_code=national_code,
                phone=phone,
                password=make_password(password),
                home_address=home_address,
                bank_name=bank_name,
                bank_card_number=bank_card_number,
                shaba_number=shaba,
                base_worksheet_count=base_worksheet_count,
                base_worksheet_salary=base_worksheet_salary,
                membership_card_number=membership_card_number,
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
            old_employee.first_name = first_name
            old_employee.last_name = last_name
            old_employee.father_name = father_name
            old_employee.national_code = national_code
            old_employee.phone = phone
            if password != '' and re_password != '':
                if password == re_password:
                    old_employee.password = make_password(password)
                else:
                    return JsonResponse({"response_code": 3, "error_msg": NOT_SIMILAR_PASSWORD})
            old_employee.home_address = home_address
            old_employee.bank_name = bank_name
            old_employee.bank_card_number = bank_card_number
            old_employee.shaba_number = shaba
            old_employee.base_worksheet_count = base_worksheet_count
            old_employee.base_worksheet_salary = base_worksheet_salary
            old_employee.membership_card_number = membership_card_number

            old_employee.save()

            old_employee_to_branch.position = position
            old_employee_to_branch.auth_level = int(auth_level)
            old_employee_to_branch.save()
            return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_employee(request):
    if request.method == "POST":
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
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def check_login(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 2})
        else:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def log_out(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if request.session.get('is_logged_in', None) == username:
            request.session['is_logged_in'] = {}
            return JsonResponse({"response_code": 2})
        else:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_employees(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            branch = rec_data['branch']
            all_employees = EmployeeToBranch.objects.filter(branch__pk=branch)
            employees = []
            for employee in all_employees:
                employees.append({
                    "id": employee.employee.pk,
                    "last_name": employee.employee.last_name,
                    "position": employee.position,
                    "auth_lvl": employee.auth_level,
                })
            return JsonResponse({"response_code": 2, 'employees': employees})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_employee(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            employee_id = rec_data['employee_id']
            employee = Employee.objects.get(pk=employee_id)
            employee_to_branch = EmployeeToBranch.objects.get(employee=employee)
            employee_data = {
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'father_name': employee.father_name,
                'national_code': employee.national_code,
                'phone': employee.phone,
                'home_address': employee.home_address,
                'bank_name': employee.bank_name,
                'bank_card_number': employee.bank_card_number,
                'shaba': employee.shaba_number,
                'position': employee_to_branch.position,
                'membership_card_number': employee.membership_card_number,
                'base_worksheet_salary': employee.base_worksheet_salary,
                'base_worksheet_count': employee.base_worksheet_count,
                'auth_level': employee_to_branch.auth_level,
            }
            return JsonResponse({"response_code": 2, 'employee': employee_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_menu_categories(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            all_menu_categories = MenuCategory.objects.all().order_by('list_order')
            menu_categories = []
            for category in all_menu_categories:
                menu_categories.append({
                    "id": category.pk,
                    "name": category.name,
                })
            return JsonResponse({"response_code": 2, 'menu_categories': menu_categories})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_menu_category(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            menu_category_id = rec_data['menu_category_id']
            menu_category = MenuCategory.objects.get(pk=menu_category_id)
            all_cat_to_printer = PrinterToCategory.objects.filter(menu_category=menu_category)

            printers = Printer.objects.all()
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
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def add_menu_category(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        menu_category_id = rec_data['menu_category_id']
        name = rec_data['name']
        kind = rec_data['kind']
        printers_id = rec_data['printers_id']
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not kind:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if menu_category_id == 0:
            new_menu_category = MenuCategory(
                name=name,
                kind=kind
            )
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
            old_menu_category_printers = PrinterToCategory.objects.filter(menu_category=old_menu_category)
            for printer in old_menu_category_printers:
                printer.delete()
            old_menu_category.name = name
            old_menu_category.kind = kind
            for printer_id in printers_id:
                printer_object = Printer.objects.get(pk=printer_id)
                new_printer_to_menu_cat = PrinterToCategory(
                    printer=printer_object,
                    menu_category=old_menu_category
                )
                new_printer_to_menu_cat.save()
            old_menu_category.save()
            return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_menu_category(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        categories_searched = MenuCategory.objects.filter(name__contains=search_word)
        menu_categories = []
        for category in categories_searched:
            menu_categories.append({
                "name": category.name,
            })
        return JsonResponse({"response_code": 2, 'menu_categories': menu_categories})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_menu_items(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            all_menu_items = MenuItem.objects.filter(is_delete=0).order_by('menu_category__name')
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
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


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
    if request.method == "POST":
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
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


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
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = MenuItem.objects.filter(name__contains=search_word, is_delete=0)
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
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        menu_items_with_categories_data = []
        menu_categories = MenuCategory.objects.all().order_by('list_order')
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
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        printers = Printer.objects.all()
        printers_data = []
        for printer in printers:
            printers_data.append({
                'printer_id': printer.pk,
                'printer_name': printer.name,
                'is_checked': 0
            })
        return JsonResponse({"response_code": 2, 'printers': printers_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


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
