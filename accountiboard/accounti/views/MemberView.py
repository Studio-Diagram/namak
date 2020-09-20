from accounti.models import *
from django.db.models.functions import Concat
from django.db.models import Value as V
from django.db import IntegrityError
from django.views import View
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.shortcuts import get_object_or_404
from django.db.models import Sum


class AddMemberView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        member_id = rec_data.get('member_id')
        first_name = rec_data.get('first_name')
        last_name = rec_data.get('last_name')
        card_number = rec_data.get('card_number')
        card_number = card_number.replace("؟", "")
        card_number = card_number.replace("٪", "")
        card_number = card_number.replace("?", "")
        card_number = card_number.replace("%", "")
        year_of_birth = rec_data.get('year_of_birth')
        month_of_birth = rec_data.get('month_of_birth')
        day_of_birth = rec_data.get('day_of_birth')
        intro = rec_data.get('intro')
        phone = rec_data.get('phone')
        branch_id = rec_data.get('branch')

        method = "None"
        member_primary_key = 0

        if not card_number:
            card_number = phone

        if not last_name or not phone or not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if member_id == 0:
            organization_object = Branch.objects.get(id=branch_id).organization
            try:
                new_member = Member(
                    first_name=first_name,
                    last_name=last_name,
                    card_number=card_number,
                    year_of_birth=year_of_birth if year_of_birth else 0,
                    month_of_birth=month_of_birth if month_of_birth else 0,
                    day_of_birth=day_of_birth if day_of_birth else 0,
                    phone=phone,
                    intro=intro,
                    organization=organization_object
                )
                new_member.save()

                method = "create"
                member_primary_key = new_member.pk
            except IntegrityError as e:
                return JsonResponse({"response_code": 3, "error_msg": DUPLICATE_MEMBER_ENTRY})

        else:
            try:
                old_member = Member.objects.get(pk=member_id)
                old_member.first_name = first_name
                old_member.last_name = last_name
                old_member.card_number = card_number
                old_member.year_of_birth = year_of_birth if year_of_birth else 0
                old_member.month_of_birth = month_of_birth if month_of_birth else 0
                old_member.day_of_birth = day_of_birth if day_of_birth else 0
                old_member.phone = phone
                old_member.intro = intro
                old_member.save()

                method = "edit"
                member_primary_key = old_member.pk

            except IntegrityError as e:
                return JsonResponse({"response_code": 3, "error_msg": DUPLICATE_MEMBER_ENTRY})

        return JsonResponse({"response_code": 2, "created_member": {
            "first_name": first_name,
            "last_name": last_name,
            "card_number": card_number,
            "method": method,
            "member_primary_key": member_primary_key
        }})


class GetMembersView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data.get('branch')
        organization_object = Branch.objects.get(id=branch_id).organization
        members = Member.objects.filter(organization=organization_object).order_by("-id")[:100]
        members_data = []
        for member in members:
            members_data.append({
                'id': member.pk,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'phone': member.phone,
                'card_number': member.card_number,
            })
        return JsonResponse({"response_code": 2, 'members': members_data})


class SearchMemberView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data.get('search_word')
        branch_id = rec_data.get('branch')
        organization_object = Branch.objects.get(id=branch_id).organization

        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Member.objects.annotate(
            full_name=Concat('first_name', V(' '), 'last_name')).filter(
            full_name__contains=search_word, organization=organization_object)
        members = []
        for member in items_searched:
            members.append({
                'id': member.pk,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'phone': member.phone,
                'card_number': member.card_number,
            })
        return JsonResponse({"response_code": 2, 'members': members})


class GetMemberView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data.get('branch')

        if rec_data.get('member_id'):
            member_id = rec_data.get('member_id')
            member = get_object_or_404(Member, pk=member_id)

        elif rec_data.get('card_number'):
            card_number = rec_data.get('card_number')
            card_number = card_number.replace("؟", "")
            card_number = card_number.replace("٪", "")
            card_number = card_number.replace("?", "")
            card_number = card_number.replace("%", "")

            organization_object = Branch.objects.get(id=branch_id).organization
            member = get_object_or_404(Member, card_number=card_number, organization=organization_object)

        else:
            return JsonResponse({}, status=404)

        member_data = {
            'id': member.pk,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'phone': member.phone,
            'year_of_birth': member.year_of_birth,
            'month_of_birth': member.month_of_birth,
            'day_of_birth': member.day_of_birth,
            'intro': member.intro,
            'card_number': member.card_number,
            'credits_data': []
        }

        total_member_credit_objects = Credit.objects.filter(member=member, expire_time__gte=datetime.now())
        all_credit_types = Credit.CATEGORIES
        for credit_type in all_credit_types:
            all_credits_from_type = total_member_credit_objects.filter(credit_categories__exact=[credit_type[0]])
            sum_all_credit_from_type = all_credits_from_type.aggregate(Sum('total_price')).get('total_price__sum')
            sum_used_credit_from_type = all_credits_from_type.aggregate(Sum('used_price')).get('used_price__sum')
            member_data.get('credits_data').append({
                'type': credit_type[0],
                'name': credit_type[1],
                'total_price': sum_all_credit_from_type if sum_all_credit_from_type else 0,
                'used_price': sum_used_credit_from_type if sum_used_credit_from_type else 0
            })

        return JsonResponse({'member': member_data})
