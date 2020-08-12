from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.views import View

class BankingView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']})
    def get(self, request, *args, **kwargs):
        branch_queryparam = request.GET.get('branch', None)
        # print(branch_queryparam, type(branch_queryparam), request.method, type(request.method))
        
        cash_register = [{'name':x.name, 'unit':x.unit} for x in CashRegister.objects.filter(branch=branch_queryparam)]
        tankhah = [{'name':x.name, 'unit':x.unit} for x in Tankhah.objects.filter(branch=branch_queryparam)]
        bank = [{'name':x.name, 'unit':x.unit, 'bank_name':x.bank_name,
        'bank_account':x.bank_account, 'bank_card_number':x.bank_card_number,
        'shaba_number':x.shaba_number} for x in Bank.objects.filter(branch=branch_queryparam)]

        return JsonResponse({
                'cash_register': cash_register,
                'tankhah': tankhah,
                'bank': bank,
        }, status=200)


    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        name   = rec_data.get('name'),
        unit   = rec_data.get('unit'),
        branch = rec_data.get('branch')
        bank_name = rec_data.get('bank_name'),
        bank_account = rec_data.get('bank_account'),
        bank_card_number = rec_data.get('bank_card_number'),
        shaba_number = rec_data.get('shaba_number'),
        type = rec_data.get('type')

        branch_obj = Branch.objects.get(pk=branch)

        if type == 'CASH_REGISTER':
            CashRegister.objects.create(
                name   = name,
                unit   = unit,
                branch = branch_obj,
            )

        elif type == 'TANKHAH':
            Tankhah.objects.create(
                name   = name,
                unit   = unit,
                branch = branch_obj,
            )

        elif type == 'BANK':
            Bank.objects.create(
                name   = name,
                unit   = unit,
                branch = branch_obj,
                bank_name = bank_name,
                bank_account = bank_account,
                bank_card_number = bank_card_number,
                shaba_number = shaba_number,
            )

        return JsonResponse({
                'msg': 'banking info added'
        }, status=200)