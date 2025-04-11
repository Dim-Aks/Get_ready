import pytest
from django import forms
from django.contrib.auth.models import User
from ..forms import ProfileUserForm, RegisterUserForm, UserPasswordChangeForm


# тестовый пользователь
@pytest.fixture
def user():
    return User.objects.create_user(
        username='Test_user',
        email='Test@mail.com',
        password='Password')


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
    def test_form_data(self, user):
        form = ProfileUserForm(instance=user)
        assert form.initial['username'] == 'Test_user'
        assert form.initial['email'] == 'Test@mail.com'

    # тест на неизменяемость полей
    @pytest.mark.django_db
    def test_disable_form(self):

        form = ProfileUserForm(data = {
            'username': 'new_user',
            'email': 'new@mail.com'
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

    # тест на уникальность email
    @pytest.mark.django_db
    def test_unique_email(self, user):
        data = {'username':'new_user',
                'email':'Test@mail.com',
                'password1':'Test_password1!',
                'password2':'Test_password2!'}
        form_uniq = RegisterUserForm(data=data)
        assert not form_uniq.is_valid()
        assert 'email' in form_uniq.errors
        assert 'Такой E-mail уже существует!' in form_uniq.errors['email']

    @pytest.mark.django_db
    @pytest.mark.parametrize('data,errors', [
    # пустые данные
    ({}, ['username', 'password1', 'password2']),

    # несовпадающие пароли
    ({
        'username': 'test_user',
        'email': 'test@mail.com',
        'password1': 'Pass123!',
        'password2': 'Pas123!'
    }, ['password2']),

    # некорректный email
    ({
        'username': 'test_user',
        'email': 'invalid-email',
        'password1': 'TestPass123!',
        'password2': 'TestPass123!'
    }, ['email']),

    # Слишком простой пароль
    ({
        'username': 'test_user',
        'email': 'test@mail.com',
        'password1': '123',
        'password2': '123'
    }, ['password2']),
])
    # тест валидности вводимых значений
    def test_valid_values(self, data, errors):
        form = RegisterUserForm(data=data)
        assert not form.is_valid()
        assert list(form.errors.keys()) == errors

    # тест успешного создания пользователя
    @pytest.mark.django_db
    def test_register_user(self):
        data = {'username': 'new_user',
                'email': 'new@mail.com',
                'password1': 'SecurePass123!',
                'password2': 'SecurePass123!'}
        form = RegisterUserForm(data=data)
        assert form.is_valid()
        new_user = form.save()
        assert User.objects.filter(username='new_user').exists()
        assert new_user.email == 'new@mail.com'
        assert new_user.check_password('SecurePass123!')

        # тест на хеширование пароля
        assert new_user.password.startswith('pbkdf2_sha256')


# тест формы смены пароля
class TestUserPasswordChangeForm:

    # тест полей формы
    def test_fields_form(self):

        # поле old_password
        old_password = UserPasswordChangeForm.base_fields['old_password']
        assert old_password.label == 'Старый пароль'
        assert isinstance(old_password.widget, forms.PasswordInput)
        assert old_password.widget.attrs['class'] == 'form-input'

        # поле new_password1
        new_password1 = UserPasswordChangeForm.base_fields['new_password1']
        assert new_password1.label == 'Новый пароль'
        assert isinstance(new_password1.widget, forms.PasswordInput)
        assert new_password1.widget.attrs['class'] == 'form-input'

        # поле new_password2
        new_password2 = UserPasswordChangeForm.base_fields['new_password2']
        assert new_password2.label == 'Подтверждение пароля'
        assert isinstance(new_password2.widget, forms.PasswordInput)
        assert new_password2.widget.attrs['class'] == 'form-input'

    # тест изменения пароля
    @pytest.mark.django_db
    def test_password_change_form(self, user):
        data = {'old_password':'Password',
                'new_password1':'NewSecurePass123!',
                'new_password2':'NewSecurePass123!'}
        form = UserPasswordChangeForm(user=user,data=data)
        assert form.is_valid()
        form.save()
        assert user.check_password('NewSecurePass123!')

    @pytest.mark.django_db
    @pytest.mark.parametrize("old_pass, new_pass1, new_pass2, errors", [
        # неверный старый пароль
        ('password', 'NewPass123!', 'NewPass123!', ['old_password']),
        # пароли не совпадают
        ('Password', 'NewPass123!', 'DifferentPass123!', ['new_password2']),
        # слишком короткий пароль
        ('Password', 'short', 'short', ['new_password2']),
        # пустые поля
        ('', '', '', ['old_password', 'new_password1', 'new_password2']),
        # слишком простой пароль
        ('Password', '12345678', '12345678', ['new_password2']),
    ])
    # тест валидации
    def test_password_valid(self, old_pass, new_pass1, new_pass2, errors, user):
        data = {
            'old_password': old_pass,
            'new_password1': new_pass1,
            'new_password2': new_pass2
        }
        form = UserPasswordChangeForm(user=user, data=data)
        assert not form.is_valid()
        assert list(form.errors.keys()) == errors