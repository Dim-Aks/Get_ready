import pytest
from django import forms
from django.contrib.auth.models import User
from ..forms import ProfileUserForm


# тестирование формы профиля пользователя в ЛК
class TestProfileUserForm:

    # тест класса мета
    def test_meta(self):
        assert ProfileUserForm.Meta.fields == ['username', 'email']
        assert ProfileUserForm.Meta.model == User

    # тест полей формы
    def test_profile_user_form(self):
        # поле username
        username_form = ProfileUserForm.base_fields['username']
        assert username_form.disabled is True
        assert username_form.label == 'Имя пользователя'
        assert isinstance(username_form.widget, forms.TextInput)
        assert username_form.widget.attrs['class'] == 'form-input'

        # поле email
        email_form = ProfileUserForm.base_fields['email']
        assert email_form.disabled is True
        assert email_form.label == 'E-mail'
        assert isinstance(email_form.widget, forms.TextInput)
        assert email_form.widget.attrs['class'] == 'form-input'

    # тест на корректность данных в форме
    # @pytest.mark.django_db
    # def test_form_data(self):
    #     pass
        # assert ProfileUserForm['username'] == 'testuser'