from accountiboard.settings import JWT_SECRET
import jwt
import datetime
import json


def make_new_JWT_token(id, phone, roles, bundle, branch_list):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
        'iat': datetime.datetime.utcnow(),
        'sub_id': id,
        'sub_phone': phone,
        'sub_roles': roles,
        'sub_bundle': bundle,
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


def get_json(response):
    """
        Parses a returned response as json when sending a request
            using 'requests' module.
    """

    return json.loads(response.content.decode('utf-8'))