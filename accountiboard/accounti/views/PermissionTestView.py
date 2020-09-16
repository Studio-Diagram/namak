from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.views import View

class FreeTestView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        set(), # Empty set allows all bundles
        branch_disable=True)
    def get(self, request, *args, **kwargs):
        print(request.payload)

        return JsonResponse({'results': 'Free bundle permission ran okay'})


class NonFreeTestView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {"FREE"}, # or USER_PLANS_CHOICES['FREE'], => prevent FREE bundles to see this view
        branch_disable=True)
    def get(self, request, *args, **kwargs):
        print(request.payload)

        return JsonResponse({'results': 'Non Free bundle permission ran okay. You must have a bundle, cool..'})
