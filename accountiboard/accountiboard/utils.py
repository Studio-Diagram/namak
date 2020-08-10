from accountiboard.settings import JWT_SECRET
import accountiboard.settings as settings
import jwt
import datetime
import base64
import random
from PIL import Image
from io import BytesIO


def make_new_JWT_token(id, phone, roles, branch_list):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
        'iat': datetime.datetime.utcnow(),
        'sub_id': id,
        'sub_phone': phone,
        'sub_roles': roles,
        'sub_branch_list': branch_list,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def decode_JWT_return_user(token):
    token = token.replace('Bearer ', '').strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload

    except Exception as e:
        return False


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
