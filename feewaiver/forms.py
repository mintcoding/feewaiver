from __future__ import unicode_literals
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth import get_user_model
from django.forms import Form, ModelForm, CharField, ValidationError, EmailField

from ledger.accounts.models import Profile, Address, Organisation


User = get_user_model()


class LoginForm(Form):
    email = EmailField(max_length=254)

