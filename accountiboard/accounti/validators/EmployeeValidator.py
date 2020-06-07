from django import forms


class LoginValidator(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)


class RegisterEmployeeValidator(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    password = forms.CharField(max_length=255, required=False)
    re_password = forms.CharField(max_length=255, required=False)
    birthday_date = forms.DateField(required=False)
    home_address = forms.CharField(max_length=2500)

    employee_id = forms.IntegerField()
    employee_roles = forms.MultipleChoiceField(required=False)
    father_name = forms.CharField(max_length=255)
    national_code = forms.CharField(max_length=30)

    bank_name = forms.CharField(max_length=255)
    bank_card_number = forms.CharField(max_length=30)
    shaba = forms.CharField(max_length=255)
    branch_id = forms.IntegerField()


class SearchEmployeeValidator(forms.Form):
    search_word = forms.CharField(max_length=255)
    branch_id = forms.IntegerField()


class AddMenuCategoryValidator(forms.Form):
    name = forms.CharField(max_length=255)
    kind = forms.CharField(max_length=255)
    printers_id = forms.IntegerField()
    branch_id = forms.IntegerField()


class AddMenuItemValidator(forms.Form):
    menu_item_id = forms.IntegerField()
    menu_category_id = forms.IntegerField()
    name = forms.CharField(max_length=255)
    price = forms.FloatField()
