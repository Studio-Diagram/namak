from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.views import View

class StocksView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def get(self, request, *args, **kwargs):
        payload = request.payload
        branch_id_list_jwt = [x['id'] for x in payload['sub_branch_list']]
        stocks = []

        stocks_to_branches = StockToBranch.objects.filter(branch__in=branch_id_list_jwt)
        stocks_list = [x.stock.id for x in stocks_to_branches]

        stocks_query = Stock.objects.filter(pk__in=stocks_list)

        for x in stocks_query:
            stocks_to_branches = StockToBranch.objects.filter(stock=x.id)
            stocks.append({'id':x.id, 'name':x.name, 'branches':[b.branch.id for b in stocks_to_branches]})

        return JsonResponse({
            'stocks': stocks,
        }, status=200)


    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        name   = rec_data.get('name')
        branches_in_request = rec_data.get('branches')
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
                

        current_stock = Stock.objects.create(
            name = name,
        )

        branch_objects = Branch.objects.filter(pk__in=branches_id_list_to_add)
        for branch_object in branch_objects:
            StockToBranch.objects.create(
                branch = branch_object,
                stock = current_stock,
            )

        return JsonResponse({
            'msg': 'stocks info added'
        }, status=200)



class StockDetailView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def get(self, request, id, *args, **kwargs):
        payload = request.payload
        branch_id_list_jwt = [x['id'] for x in payload['sub_branch_list']]

        stocks_to_branches = StockToBranch.objects.filter(branch__in=branch_id_list_jwt)

        for stock_to_branch in stocks_to_branches:
            if stock_to_branch.stock.id == id:

                all_branches_this_stock = StockToBranch.objects.filter(stock=stock_to_branch.stock)
                branch_list = [x.branch.id for x in all_branches_this_stock]
                try:
                    current_stock = Stock.objects.get(pk=id)
                    return JsonResponse({
                        'id' : current_stock.id,
                        'branches' : branch_list,
                        'name' : current_stock.name,
                    }, status=200)
                except:
                    return JsonResponse({
                            'error_msg': BANKING_NOT_FOUND,
                    }, status=404)


class StockByBranchView(View):
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

        banking_to_branch = StockToBranch.objects.filter(branch=current_branch)
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