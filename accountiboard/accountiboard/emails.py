from django.core.mail import send_mail
from django.conf import settings

def send_expiry_email(receiver_email, num_of_days):
    send_mail(
        'نمک : بسته فعال شما به زودی منقضی می شود ',
        f"""
        بسته فعال شما پس از {num_of_days} روز دیگر منقضی می شود.
        \n\nلطفا جهت خرید بسته جدید اقدام کنید.
        \n\nنمک""",
        settings.SERVER_EMAIL,
        [receiver_email],
        fail_silently=False,
    )
