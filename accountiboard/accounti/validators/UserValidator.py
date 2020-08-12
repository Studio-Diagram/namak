from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from accountiboard.constants import *


class RegisterUserValidator(forms.Form):
    company_name = forms.CharField(max_length=255,
                                   error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    phone = forms.CharField(max_length=30, error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    email = forms.EmailField(error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    password = forms.CharField(max_length=255,
                               error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    re_password = forms.CharField(max_length=255,
                                  error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})


class RegisterCafeOwnerValidator(forms.Form):
    first_name = forms.CharField(max_length=255,
                                 error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    last_name = forms.CharField(max_length=255,
                                error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    company_name = forms.CharField(max_length=255,
                                   error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    phone = forms.CharField(max_length=30, error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    password = forms.CharField(max_length=255,
                               error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    re_password = forms.CharField(max_length=255,
                                  error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    sms_verify_token = forms.CharField(max_length=10,
                                  error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})


class ForgotPasswordValidator(forms.Form):
    phone = forms.CharField(max_length=30, error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    password = forms.CharField(max_length=255,
                               error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    re_password = forms.CharField(max_length=255,
                                  error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    sms_verify_token = forms.CharField(max_length=10,
                                  error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})


class ProfileValidator(forms.Form):
    first_name = forms.CharField(max_length=255,
                                 error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    last_name = forms.CharField(max_length=255,
                                error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    phone = forms.CharField(max_length=30, error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    email = forms.EmailField(error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})


class PasswordValidator:
    def __init__(self, min_digits=0):
        self.min_digits = min_digits
        self.errors = []

    def validate(self, password):
        try:
            validate_password(password)
            if not len(password) >= self.min_digits:
                self.errors.append(PASSWORD_WEAK)
                return False
            return True
        except ValidationError as e:
            self.errors = e
            return False

    def validate_with_re_password(self, password, re_password):
        if password != re_password:
            self.errors.append(NOT_SIMILAR_PASSWORD)
            return False
        return True

    def get_errors(self):
        return [{"password": error} for error in self.errors]



class PhoneNumberValidator:
    def __init__(self):
        self.errors = []

    def validate(self, phone):
        if len(phone) < 11:
            self.errors.append(PHONE_TOO_FEW_CHARACTERS)
        elif len(phone) > 13:
            self.errors.append(PHONE_TOO_MANY_CHARACTERS)

        if phone[:2] != '09':
            self.errors.append(PHONE_DOESNT_START_WITH_09)

    def get_errors(self):
        return [error for error in self.errors]