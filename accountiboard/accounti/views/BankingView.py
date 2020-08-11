from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.views import View

class BankingView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      branch_disable=True)
    def get(self, request, *args, **kwargs):
        pass


    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch = rec_data.get('branch')
        cash_register = rec_data.get('cash_register')
        tankhah = rec_data.get('tankhah')
        bank = rec_data.get('bank')

        branch_obj = Branch.objects.get(pk=branch)

        if cash_register:
            CashRegister.objects.create(
                name   = cash_register.get('name'),
                unit   = cash_register.get('unit'),
                branch = branch_obj,
            )

        if tankhah:
            Tankhah.objects.create(
                name   = tankhah.get('name'),
                unit   = tankhah.get('unit'),
                branch = branch_obj,
            )

        if bank:
            Bank.objects.create(
                name   = bank.get('name'),
                unit   = bank.get('unit'),
                branch = branch_obj,
                bank_name = bank.get('bank_name'),
                bank_account = bank.get('bank_account'),
                bank_card_number = bank.get('bank_card_number'),
                shaba_number = bank.get('shaba_number'),
            )

        return JsonResponse({
                'msg': 'banking info added'
        }, status=200)