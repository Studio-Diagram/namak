import requests
from django.conf import settings
from accounti.models import *
import string
import secrets


def send_expiry_sms(receiver_phone, num_of_days):
    r1 = requests.post(settings.SMSIR_TOKEN_URL, json=settings.SMSIR_TOKEN_REQUEST)
    token_json_response = r1.json()

    if token_json_response['IsSuccessful']:
        data = {
            "ParameterArray": [
                {
                    "Parameter": "VerificationCode",
                    "ParameterValue": "123654",
                }
            ],
            "Mobile": receiver_phone,
            "TemplateId": "31173",
        }

        r2 = requests.post(settings.SMSIR_ULTRAFAST_SEND_URL, json=data,
                           headers={'x-sms-ir-secure-token': token_json_response['TokenKey']})


def send_verify_phone_sms(receiver_phone, sms_template):
    alphabet = string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(5))

    SmsToken.objects.create(
        phone=receiver_phone,
        token=token,
    )

    if not settings.DEBUG:
        r1 = requests.post(settings.SMSIR_TOKEN_URL, json=settings.SMSIR_TOKEN_REQUEST)
        token_json_response = r1.json()

        if token_json_response['IsSuccessful']:
            data = {
                "ParameterArray": [
                    {
                        "Parameter": "VerificationCode",
                        "ParameterValue": token,
                    }
                ],
                "Mobile": receiver_phone,
                "TemplateId": sms_template,
            }

            r2 = requests.post(settings.SMSIR_ULTRAFAST_SEND_URL, json=data,
                               headers={'x-sms-ir-secure-token': token_json_response['TokenKey']})

    elif settings.DEBUG:
        print(token)
