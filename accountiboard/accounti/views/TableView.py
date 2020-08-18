from django.http import JsonResponse
import json
from accounti.models import *
from accountiboard.constants import *
from django.db import IntegrityError


def add_table(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        table_id = rec_data['table_id']
        table_cat_id = rec_data['table_cat_id']
        name = rec_data['name']

        if not name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not table_cat_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        table_cat_obj = TableCategory.objects.filter(id=table_cat_id).first()
        all_tables_in_branch = Table.objects.filter(category__branch=table_cat_obj.branch, name=name)

        if all_tables_in_branch.count():
            return JsonResponse({"response_code": 3, "error_msg": UNIQUE_VIOLATION_ERROR})

        if table_id == 0:
            new_table = Table(
                name=name,
                category=table_cat_obj
            )
            try:
                new_table.save()
            except IntegrityError:
                return JsonResponse({"response_code": 3, "error_msg": UNIQUE_VIOLATION_ERROR})

            return JsonResponse({"response_code": 2})
        else:
            old_table = Table.objects.get(pk=table_id)
            old_table.name = name
            old_table.category = table_cat_obj
            old_table.save()
            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_table(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Table.objects.filter(name__contains=search_word)
        tables = []
        for table in items_searched:
            tables.append({
                'table_id': table.pk,
                'table_name': table.name,
                'table_cat_name': table.category.name,
            })
        return JsonResponse({"response_code": 2, 'tables': tables})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_table(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        table_id = rec_data['table_id']
        table = Table.objects.get(pk=table_id)
        table_data = {
            'table_id': table.pk,
            'table_name': table.name,
            'table_cat_id': table.category.id,
        }
        return JsonResponse({"response_code": 2, 'table': table_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def add_table_category(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    name = rec_data.get('name')
    table_cat_id = rec_data.get('id')
    branch_id = rec_data.get('branch')

    if not name or not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    if table_cat_id == 0:
        new_table_category = TableCategory(
            name=name,
            branch_id=branch_id
        )
        try:
            new_table_category.save()
        except IntegrityError:
            return JsonResponse({"response_code": 3, "error_msg": UNIQUE_VIOLATION_ERROR})

        return JsonResponse({"response_code": 2})
    else:
        old_table_cat = TableCategory.objects.get(pk=table_cat_id)
        old_table_cat.name = name
        old_table_cat.save()
        return JsonResponse({"response_code": 2})


def get_tables(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    tables = Table.objects.filter(category__branch_id=branch_id).order_by('id')
    tables_data = []
    for table in tables:
        tables_data.append({
            'table_id': table.pk,
            'table_name': table.name,
            'table_category_name': table.category.name,
            'is_checked': 0
        })
    return JsonResponse({"response_code": 2, 'tables': tables_data})


def get_table_category(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    table_cat_id = rec_data.get('table_cat_id')

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    if not table_cat_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    table_cat = TableCategory.objects.get(pk=table_cat_id)
    table_cat_data = {
        'id': table_cat.pk,
        'name': table_cat.name,
    }
    return JsonResponse({"response_code": 2, 'table_category': table_cat_data})


def get_table_categories(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    table_cats = TableCategory.objects.filter(branch_id=branch_id).order_by('id')
    table_cats_data = []
    for cat in table_cats:
        table_cats_data.append({
            'id': cat.pk,
            'name': cat.name,
        })
    return JsonResponse({"response_code": 2, 'table_categories': table_cats_data})
