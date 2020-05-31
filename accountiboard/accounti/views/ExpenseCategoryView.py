from django.http import JsonResponse
import json, base64, random
from accounti.models import *
import accountiboard.settings as settings
from PIL import Image
from io import BytesIO
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from accountiboard.constants import *


def add_expense_category(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        expense_cat_id = rec_data['expense_cat_id']
        name = rec_data['name']
        if not name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if expense_cat_id == 0:
            new_expense_cat = ExpenseCategory(
                name=name,
            )
            new_expense_cat.save()
            return JsonResponse({"response_code": 2})
        else:
            old_expense_cat = ExpenseCategory.objects.get(pk=expense_cat_id)
            old_expense_cat.name = name
            old_expense_cat.save()
            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_all_expense_categories(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        all_expense_categories = ExpenseCategory.objects.all()
        expenses_data = []
        for cat in all_expense_categories:
            expenses_data.append({
                'id': cat.pk,
                'name': cat.name,
            })
        return JsonResponse({"response_code": 2, 'all_expense_categories': expenses_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_expense_category(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = ExpenseCategory.objects.filter(name__contains=search_word)
        expenses = []
        for branch in items_searched:
            expenses.append({
                "id": branch.pk,
                "name": branch.name,
            })
        return JsonResponse({"response_code": 2, 'all_expense_categories': expenses})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_expense_category(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        expense_category_id = rec_data['expense_cat_id']
        expense_cat = ExpenseCategory.objects.get(pk=expense_category_id)
        expense_cat_data = {
            'id': expense_cat.pk,
            'name': expense_cat.name,
        }
        return JsonResponse({"response_code": 2, 'expense_category': expense_cat_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
