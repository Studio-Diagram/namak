from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
from accountiboard.emails import *
from accountiboard.sms import *
from accounti.models import *


def check_bundles():
    active_bundles = Bundle.objects.filter(is_active=True)

    for bundle in active_bundles:

        if now() + timedelta(days=7, seconds=5) > bundle.expiry_datetime_plan:
            if bundle.cafe_owner.user.email:
                send_expiry_email(bundle.cafe_owner.user.email, 7)

            send_expiry_sms(bundle.cafe_owner.user.phone, 7)

        elif now() + timedelta(days=3, seconds=5) > bundle.expiry_datetime_plan:
            if bundle.cafe_owner.user.email:
                send_expiry_email(bundle.cafe_owner.user.email, 3)

            send_expiry_sms(bundle.cafe_owner.user.phone, 3)

        elif now() + timedelta(days=1, seconds=5) > bundle.expiry_datetime_plan:
            if bundle.cafe_owner.user.email:
                send_expiry_email(bundle.cafe_owner.user.email, 1)

            send_expiry_sms(bundle.cafe_owner.user.phone, 1)

        elif now() > bundle.expiry_datetime_plan:
            # expire active plan
            bundle.is_expired = True
            bundle.is_active = False
            bundle.save()

            # activate a reserved bundle if cafe owner has one
            try:
                this_cafe_owner_reserved_bundle = Bundle.objects.get(cafe_owner=bundle.cafe_owner, is_reserved=True)
                this_cafe_owner_reserved_bundle.is_active = True
                this_cafe_owner_reserved_bundle.is_reserved = False
                this_cafe_owner_reserved_bundle.save()
            except:
                pass



