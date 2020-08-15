from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.views import View

class BankingView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      branch_disable=True)
    def get(self, request, *args, **kwargs):
        payload = request.payload
        branch_id_list = [x['id'] for x in payload['sub_branch_list']]
        cash_register = []
        tankhah = []
        bank = []

        banking_to_branches = BankingToBranch.objects.filter(branch__in=branch_id_list)

        for banking_to_branch in banking_to_branches:
            
            cash_register.extend([{'id':x.id, 'name':x.name, 'unit':x.unit} for x in CashRegister.objects.filter(pk=banking_to_branch.banking)])
            tankhah.extend([{'id':x.id, 'name':x.name, 'unit':x.unit} for x in Tankhah.objects.filter(pk=banking_to_branch.banking)])
            bank.extend([{'id':x.id, 'name':x.name, 'unit':x.unit, 'bank_name':x.bank_name,
            'bank_account':x.bank_account, 'bank_card_number':x.bank_card_number,
            'shaba_number':x.shaba_number} for x in Bank.objects.filter(pk=banking_to_branch.banking)])

        return JsonResponse({
                'cash_register': cash_register,
                'tankhah': tankhah,
                'bank': bank,
        }, status=200)


    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        name   = rec_data.get('name')
        unit   = rec_data.get('unit')
        branch = rec_data.get('branch')
        bank_name = rec_data.get('bank_name')
        bank_account = rec_data.get('bank_account')
        bank_card_number = rec_data.get('bank_card_number')
        shaba_number = rec_data.get('shaba_number')
        type = rec_data.get('type')

        branch_obj = Branch.objects.get(pk=branch)

        if type == 'CASH_REGISTER':
            current_banking = CashRegister.objects.create(
                name   = name,
                unit   = unit,
            )

        elif type == 'TANKHAH':
            current_banking = Tankhah.objects.create(
                name   = name,
                unit   = unit,
            )

        elif type == 'BANK':
            current_banking = Bank.objects.create(
                name   = name,
                unit   = unit,
                bank_name = bank_name,
                bank_account = bank_account,
                bank_card_number = bank_card_number,
                shaba_number = shaba_number,
            )

        else:
            return JsonResponse({
                    'msg': 'type not recognized'
            }, status=400)

        BankingToBranch.objects.create(
            branch = branch_obj,
            banking = current_banking,
        )


        return JsonResponse({
                'msg': 'banking info added'
        }, status=200)