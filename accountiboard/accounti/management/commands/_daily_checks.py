from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
from accounti.management.commands._emails import *
from accounti.models import *


def check_bundles():
    active_bundles = Bundle.objects.filter(is_active=True)

    for bundle in active_bundles:

        if now() + timedelta(days=7, seconds=5) > bundle.expiry_datetime_plan:
            if bundle.cafe_owner.user.email:
                send_expiry_email(bundle.cafe_owner.user.email, 7)

            # send 7 days remaining sms

        elif now() + timedelta(days=3, seconds=5) > bundle.expiry_datetime_plan:
            if bundle.cafe_owner.user.email:
                send_expiry_email(bundle.cafe_owner.user.email, 3)

            # send 3 days remaining sms

        elif now() + timedelta(days=1, seconds=5) > bundle.expiry_datetime_plan:
            if bundle.cafe_owner.user.email:
                send_expiry_email(bundle.cafe_owner.user.email, 1)

            # send 1 day remaining sms

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



