from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from accountiboard.constants import PASSWORD_WEAK, NOT_SIMILAR_PASSWORD
from accountiboard.constants import CHARACHTER_TOO_LONG, DATA_REQUIRE


class RegisterUserValidator(forms.Form):
    company_name = forms.CharField(max_length=255,
                                   error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    phone = forms.CharField(max_length=30, error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    email = forms.EmailField(error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    password = forms.CharField(max_length=255,
                               error_messages={'invalid': CHARACHTER_TOO_LONG, 'required': DATA_REQUIRE})
    re_password = forms.CharField(max_length=255,
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
