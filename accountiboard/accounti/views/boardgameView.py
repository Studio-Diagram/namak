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


def add_boardgame(request):
    f = open("/home/ubuntu/test_pythons/demofile3.txt", "r")
    all_bg = f.read()
    all_bg_list = all_bg.split("###@@@###")
    branch_obj = Branch.objects.get(pk=1)
    for bg in all_bg_list:
        bg_data = eval(bg)
        image_bg = bg_data['image']
        image_bg = image_bg.replace("./", "")
        new_boardgame = Boardgame(
            name=bg_data['name'],
            category=bg_data['cat'],
            min_players=bg_data['min_p'],
            max_players=bg_data['max_p'],
            best_players=bg_data['best_p'],
            rate=bg_data['rate'],
            learning_time=bg_data['learn'],
            duration=bg_data['dur'],
            description=bg_data['discription'],
            bgg_code=bg_data['bgg_code'],
            branch=branch_obj,
            image=image_bg,
            image_name=image_bg
        )
        new_boardgame.save()

    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        boardgame_id = rec_data['boardgame_id']
        name = rec_data['name']
        category = rec_data['category']
        min_players = rec_data['min_players']
        max_players = rec_data['max_players']
        best_players = rec_data['best_players']
        rate = rec_data['rate']
        learning_time = rec_data['learning_time']
        duration = rec_data['duration']
        image_name = rec_data['image_name']
        image_path = rec_data['image_path']
        description = rec_data['description']
        bgg_code = rec_data['bgg_code']
        branch_id = rec_data['branch']

        # if not boardgame_id:
         #   return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not category:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not min_players:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not max_players:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not best_players:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not rate:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not learning_time:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not duration:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not image_name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not image_path:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not bgg_code:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)

        new_boardgame = Boardgame(
            name=name,
            category=category,
            min_players=min_players,
            max_players=max_players,
            best_players=best_players,
            rate=rate,
            learning_time=learning_time,
            duration=duration,
            description=description,
            bgg_code=bgg_code,
            branch=branch_obj,
            image=base64_to_image(image_path, 1),
            image_name=image_name
        )
        new_boardgame.save()

        return JsonResponse({"response_code": 2})

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


def get_boardgames(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch']
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        branch_obj = Branch.objects.get(pk=branch_id)
        boardgames = Boardgame.objects.filter(branch=branch_obj)
        boardgames_data = []
        for bg in boardgames:
            boardgames_data.append({
                'id': bg.pk,
                'name': bg.name,
                'category': bg.get_category_display(),
            })
        return JsonResponse({"response_code": 2, 'boardgames': boardgames_data})


def search_boardgame(request):
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
        items_searched = Boardgame.objects.filter(name__contains=search_word, branch=branch_obj)
        boardgames = []
        for bg in items_searched:
            boardgames.append({
                "id": bg.pk,
                "name": bg.name,
                "category": bg.get_category_display(),
            })
        return JsonResponse({"response_code": 2, 'boardgames': boardgames})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_boardgame(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            boardgame_id = rec_data['boardgame_id']
            boardgame = Boardgame.objects.get(pk=boardgame_id)
            boardgame_data = {
                'id': boardgame.pk,
                'name': boardgame.name,
                'category': boardgame.category,
                'min_players': boardgame.min_players,
                'max_players': boardgame.max_players,
                'best_players': boardgame.best_players,
                'rate': boardgame.rate,
                'learning_time': boardgame.learning_time,
                'duration': boardgame.duration,
                'image_name': boardgame.image.name,
                'image_path': "/media/" + boardgame.image.url,
                'description': boardgame.description,
                'bgg_code': boardgame.bgg_code,
            }
            return JsonResponse({"response_code": 2, 'boardgame': boardgame_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

