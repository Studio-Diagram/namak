from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.views import View

class BankingView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def get(self, request, *args, **kwargs):
        payload = request.payload
        branch_id_list_jwt = [x['id'] for x in payload['sub_branch_list']]
        cash_register = []
        tankhah = []
        bank = []

        banking_to_branches = BankingToBranch.objects.filter(branch__in=branch_id_list_jwt)
        bankings_list = [x.banking for x in banking_to_branches]

        cash_registers_query = CashRegister.objects.filter(pk__in=bankings_list)
        tankhahs_query = Tankhah.objects.filter(pk__in=bankings_list)
        banks_query = Bank.objects.filter(pk__in=bankings_list)

        for x in cash_registers_query:
            banking_to_branches = BankingToBranch.objects.filter(banking=x.id)
            cash_register.append({'id':x.id, 'name':x.name, 'unit':x.unit, 'branches':[b.branch.id for b in banking_to_branches]})

        for x in tankhahs_query:
            banking_to_branches = BankingToBranch.objects.filter(banking=x.id)
            tankhah.append({'id':x.id, 'name':x.name, 'unit':x.unit, 'branches':[b.branch.id for b in banking_to_branches]})

        for x in banks_query:
            banking_to_branches = BankingToBranch.objects.filter(banking=x.id)
            bank.append({'id':x.id, 'name':x.name, 'unit':x.unit, 'bank_name':x.bank_name,
            'bank_account':x.bank_account, 'bank_card_number':x.bank_card_number,
            'shaba_number':x.shaba_number, 'branches':[b.branch.id for b in banking_to_branches]})


        return JsonResponse({
                'cash_register': cash_register,
                'tankhah': tankhah,
                'bank': bank,
        }, status=200)


    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        name   = rec_data.get('name')
        unit   = rec_data.get('unit')
        branches_in_request = rec_data.get('branches')
        bank_name = rec_data.get('bank_name')
        bank_account = rec_data.get('bank_account')
        bank_card_number = rec_data.get('bank_card_number')
        shaba_number = rec_data.get('shaba_number')
        type = rec_data.get('type')
        payload = request.payload
        branch_id_list_jwt = {x['id'] for x in payload['sub_branch_list']}
        branches_id_list_to_add = []

        if not branches_in_request or not name:
            return JsonResponse({
                'error_msg': DATA_REQUIRE
            }, status=401)

        for branch in branches_in_request:
            if branch['id'] not in branch_id_list_jwt:
                return JsonResponse({
                    'error_msg': ACCESS_DENIED
                }, status=401)
            elif 'is_checked' in branch and branch['is_checked']:
                branches_id_list_to_add.append(branch['id'])

        if not branches_id_list_to_add:
            return JsonResponse({
                'error_msg': DATA_REQUIRE_BRANCH
            }, status=401)
                

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
                'error_msg': DATA_REQUIRE
            }, status=400)

        branch_objects = Branch.objects.filter(pk__in=branches_id_list_to_add)
        for branch_object in branch_objects:
            BankingToBranch.objects.create(
                branch = branch_object,
                banking = current_banking,
            )


        return JsonResponse({
            'msg': 'banking info added'
        }, status=200)



class BankingDetailView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def get(self, request, id, *args, **kwargs):
        payload = request.payload
        branch_id_list_jwt = [x['id'] for x in payload['sub_branch_list']]
        current_banking_bank = None
        current_banking_cash = None
        current_banking_tankhah = None

        banking_to_branches = BankingToBranch.objects.filter(branch__in=branch_id_list_jwt)

        for banking_to_branch in banking_to_branches:
            if banking_to_branch.banking.id == id:

                all_branches_this_banking = BankingToBranch.objects.filter(banking=banking_to_branch.banking)
                branch_list = [x.branch.id for x in all_branches_this_banking]
                try:
                    current_banking_bank = Bank.objects.get(pk=id)
                    return JsonResponse({
                        'id' : current_banking_bank.id,
                        'type' : 'BANK',
                        'branches' : branch_list,
                        'name' : current_banking_bank.name,
                        'unit' : current_banking_bank.unit,
                        'bank_name' : current_banking_bank.bank_name,
                        'bank_account' : current_banking_bank.bank_account,
                        'bank_card_number' : current_banking_bank.bank_card_number,
                        'shaba_number' : current_banking_bank.shaba_number,
                    }, status=200)
                except:
                    pass

                try:
                    current_banking_cash = CashRegister.objects.get(pk=id)
                    return JsonResponse({
                        'id' : current_banking_cash.id,
                        'type' : 'CASH_REGISTER',
                        'branches' : branch_list,
                        'name' : current_banking_cash.name,
                        'unit' : current_banking_cash.unit,
                    }, status=200)
                except:
                    pass

                try:
                    current_banking_tankhah = Tankhah.objects.get(pk=id)
                    return JsonResponse({
                        'id' : current_banking_tankhah.id,
                        'type' : 'TANKHAH',
                        'branches' : branch_list,
                        'name' : current_banking_tankhah.name,
                        'unit' : current_banking_tankhah.unit,
                    }, status=200)
                except:
                    pass

            
        return JsonResponse({
                'error_msg': BANKING_NOT_FOUND,
        }, status=404)



class BankingByBranchView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def get(self, request, branch_id, *args, **kwargs):
        payload = request.payload
        branch_id_list_jwt = {x['id'] for x in payload['sub_branch_list']}
        cash_register = []
        tankhah = []
        bank = []

        if not branch_id:
            return JsonResponse({
                'error_msg': DATA_REQUIRE
            }, status=400)

        current_branch = int(branch_id)

        if current_branch not in branch_id_list_jwt:
            return JsonResponse({
                'error_msg': ACCESS_DENIED
            }, status=403)

        banking_to_branch = BankingToBranch.objects.filter(branch=current_branch)
        bankings_list = [x.banking for x in banking_to_branch]

        cash_registers_query = CashRegister.objects.filter(pk__in=bankings_list)
        tankhahs_query = Tankhah.objects.filter(pk__in=bankings_list)
        banks_query = Bank.objects.filter(pk__in=bankings_list)

        for x in cash_registers_query:
            cash_register.append({'id':x.id, 'name':x.name, 'type':'CASH_REGISTER', })

        for x in tankhahs_query:
            tankhah.append({'id':x.id, 'name':x.name, 'type':'TANKHAH'})

        for x in banks_query:
            bank.append({'id':x.id, 'name':x.name, 'type':'BANK'})

        return JsonResponse({
                'cash_register': cash_register,
                'tankhah': tankhah,
                'bank': bank,
        }, status=200)