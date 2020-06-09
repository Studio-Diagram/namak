from django import forms

class Login_Validator(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

class Register_Employee_Validator(forms.Form):
    EMPLOYEE_ROLE_CHOICES = (
        ('MANAGER', 'MANAGER'),
        ('CASHIER', 'CASHIER'),
        ('ACCOUNTANT', 'ACCOUNTANT'),
        ('STAFF', 'STAFF')
    )
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(max_length=255)
    re_password = forms.CharField(max_length=255)
    birthday_date = forms.DateField(required=False)
    home_address = forms.CharField(max_length=2500)

    employee_id = forms.IntegerField()
    employee_roles = forms.MultipleChoiceField(required=False, choices=EMPLOYEE_ROLE_CHOICES)
    father_name = forms.CharField(max_length=255)
    national_code = forms.CharField(max_length=30)
    position = forms.CharField(max_length=255)

    bank_name = forms.CharField(max_length=255)
    bank_card_number = forms.CharField(max_length=30)
    shaba = forms.CharField(max_length=255)
    auth_level = forms.IntegerField()
    branch_id = forms.IntegerField()

class Search_Employee_Validator(forms.Form):
    search_word = forms.CharField(max_length=255)
    branch_id = forms.IntegerField()

class Add_Menu_Category_Validator(forms.Form):
    name = forms.CharField(max_length=255)
    kind = forms.CharField(max_length=255)
    printers_id = forms.IntegerField()
    branch_id = forms.IntegerField()

class Add_Menu_Item_Validator(forms.Form):
    menu_item_id = forms.IntegerField()
    menu_category_id = forms.IntegerField()
    name = forms.CharField(max_length=255)
    price = forms.FloatField()

