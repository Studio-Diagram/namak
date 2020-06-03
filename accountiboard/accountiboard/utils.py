from accountiboard.settings import JWT_SECRET
import jwt
import datetime


def make_new_JWT_token(id, phone, roles, branch):
    payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub_id': id, 
            'sub_phone': phone,
            'sub_roles' : roles,
            'sub_branch' : branch,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def decode_JWT_return_user(token):
    token = token.replace('Bearer ','').strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload

    except Exception as e:
        return False