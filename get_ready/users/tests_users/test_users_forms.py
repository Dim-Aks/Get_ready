import pytest
from django import forms
from django.contrib.auth.models import User
from ..forms import ProfileUserForm, RegisterUserForm, UserPasswordChangeForm


# тестовый пользователь
# @pytest.fixture()
# def user():
#     return User.objects.create(
#         username='Test_user',
#         password='Password')


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
    @pytest.mark.django_db
    def test_form_data(self):
        t_user = User.objects.create(username='testuser', email='test@test.com')
        form = ProfileUserForm(instance=t_user)
        assert form.initial['username'] == 'testuser'
        assert form.initial['email'] == 'test@test.com'

    # тест на неизменяемость полей
    @pytest.mark.django_db
    def test_disable_form(self):

        form = ProfileUserForm(data = {
            'username': 'new_user',
            'email': 'new@test.com'
        })
        assert form.is_valid() is False
        assert 'username' in form.errors
        assert 'email' in form.errors

# тестирование формы регистрации пользователя
class TestRegisterUserForm:

    # тест класса мета
    def test_meta_data(self):
        assert RegisterUserForm.Meta.model == User
        assert RegisterUserForm.Meta.fields == ['username', 'email', 'password1', 'password2']
        assert RegisterUserForm.Meta.labels == {'email': 'E-mail', }
        assert RegisterUserForm.Meta.widgets['email'].attrs['class'] == 'form-input'

    # тест полей формы
    def test_form_field(self):

        # поле username
        username_form = RegisterUserForm.base_fields['username']
        assert username_form.label == 'Имя пользователя'
        assert isinstance(username_form.widget, forms.TextInput)
        assert username_form.widget.attrs['class'] == 'form-input'

        # поле password1
        password1_form = RegisterUserForm.base_fields['password1']
        assert password1_form.label == 'Пароль'
        assert isinstance(password1_form.widget, forms.PasswordInput)
        assert password1_form.widget.attrs['class'] == 'form-input'

        # поле password2
        password2_form = RegisterUserForm.base_fields['password2']
        assert password2_form.label == 'Повтор пароля'
        assert isinstance(password2_form.widget, forms.PasswordInput)
        assert password2_form.widget.attrs['class'] == 'form-input'

    # тест
    # @pytest.mark.django_db
    # def test_clean_email(self):
    #     data = {'username':'Test_user',
    #             'email':'Test@test.com',
    #             'password1':'Test_password1',
    #             'password2':'Test_password2'}
    #     form_uniq = RegisterUserForm(data=data)
    #     assert form_uniq.is_valid() is False
