import requests
from django.conf import settings

def send_expiry_sms(receiver_phone, num_of_days):
    r1 = requests.post(settings.SMSIR_TOKEN_URL, data=settings.SMSIR_TOKEN_REQUEST)
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
            "TemplateId" : "31173",
        }

        r2 = requests.post(settings.SMSIR_ULTRAFAST_SEND_URL, json=data, headers={'x-sms-ir-secure-token':token_json_response['TokenKey']})
