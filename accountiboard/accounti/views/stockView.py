from django.http import JsonResponse
import json, base64, random
from accounti.models import *
import accountiboard.settings as settings
from PIL import Image
from io import BytesIO
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'


def add_stock(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        stock_id = rec_data['stock_id']
        name = rec_data['name']
        branch_id = rec_data['branch']
        if not name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if stock_id == 0:
            branch_obj = Branch.objects.get(pk=branch_id)
            new_stock = Stock(
                name=name,
            )
            new_stock.save()
            new_stock_to_branch = StockToBranch(
                branch=branch_obj,
                stock=new_stock
            )
            new_stock_to_branch.save()

            return JsonResponse({"response_code": 2})
        else:
            old_stock = Stock.objects.get(pk=stock_id)
            old_stock.name = name
            old_stock.save()

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def base64_to_image(base64image, qid):
    allowed_formats = ['jpeg', 'png', 'gif', 'jpg']
    is_acceptable = False
    if base64image == '':
        return base64image

    if len(base64image) < 500 and (base64image[-5:] == '.jpeg' or base64image[-4:] == '.jpg' or
                                           base64image[-4:] == '.png' or base64image[-4:] == '.gif'):
        return base64image.split('/')[-1]

    for ext in allowed_formats:
        if base64image.startswith("data:image/" + ext + ";base64,"):
            is_acceptable = True
            break
    if not is_acceptable or len(base64image) > 4000000:
        return 'error'

    prefix, image_str = base64image.split(';base64,')
    decoded_string = base64.b64decode(image_str)
    if len(decoded_string) > 2000000:
        return 'error'

    name = 'image-' + hex(qid * 739 + 131 + random.randrange(1000))[2:]
    if prefix.split("/")[-1] in allowed_formats:
        name = name + "." + prefix.split("/")[-1]
    else:
        return 'error'

    img = Image.open(BytesIO(decoded_string))

    if name.endswith(".gif"):
        try:
            img.save(settings.MEDIA_ROOT + '/' + name, 'GIF', save_all=True)
        except:
            try:
                img.save(settings.MEDIA_ROOT + '/' + name, 'GIF')
            except:
                return 'error'
    else:
        base_width = min(800, img.size[0])
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        base_height = min(500, h_size)
        w_percent = (base_height / float(h_size))
        w_size = int(float(base_width) * float(w_percent))
        img = img.resize((w_size, base_height), Image.ANTIALIAS)
        img.save(settings.MEDIA_ROOT + '/' + name)
    return name


def get_stocks(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch']
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        branch_obj = Branch.objects.get(pk=branch_id)
        stocks = stock.objects.filter(branch=branch_obj)
        stocks_data = []
        for bg in stocks:
            stocks_data.append({
                'id': bg.pk,
                'name': bg.name,
                'category': bg.get_category_display(),
            })
        return JsonResponse({"response_code": 2, 'stocks': stocks_data})


def search_stock(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        branch_id = rec_data['branch']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        branch_obj = Branch.objects.get(pk=branch_id)
        items_searched = stock.objects.filter(name__contains=search_word, branch=branch_obj)
        stocks = []
        for bg in items_searched:
            stocks.append({
                "id": bg.pk,
                "name": bg.name,
                "category": bg.get_category_display(),
            })
        return JsonResponse({"response_code": 2, 'stocks': stocks})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_stock(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            stock_id = rec_data['stock_id']
            stock = stock.objects.get(pk=stock_id)
            stock_data = {
                'id': stock.pk,
                'name': stock.name,
                'category': stock.category,
                'min_players': stock.min_players,
                'max_players': stock.max_players,
                'best_players': stock.best_players,
                'rate': stock.rate,
                'learning_time': stock.learning_time,
                'duration': stock.duration,
                'image_name': stock.image.name,
                'image_path': stock.image.path,
                'description': stock.description,
                'bgg_code': stock.bgg_code,
            }
            return JsonResponse({"response_code": 2, 'stock': stock_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

