from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from accountiboard.utils import *
from django.views import View


class BugReportView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'],
                                       USER_ROLES['ACCOUNTANT'], USER_ROLES['CASHIER'],
                                       USER_ROLES['STAFF']},
                                      branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        title = rec_data.get('title')
        text = rec_data.get('text')
        image = rec_data.get('image')
        image_name = rec_data.get('image_name')
        payload = request.payload

        if not title or not text:
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        new_bugreport = BugReport.objects.create(
            title=title,
            text=text,
            user=User.objects.get(phone=payload['sub_phone']),
            image=base64_to_image(image, 1),
            image_name=image_name,
        )

        return JsonResponse({'msg': 'Bug report was successfully created'}, status=200)
