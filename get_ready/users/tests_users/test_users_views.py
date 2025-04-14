import pytest
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

from ..forms import RegisterUserForm, UserPasswordChangeForm
from ..views import ProfileUser, LoginUser, RegisterUser, UserPasswordChange


# тестовый пользователь
@pytest.fixture()
def user():
    return User.objects.create_user(
        username='Test_user',
        email='Test@mail.com',
        password='Password')


# тест профиля пользователя
@pytest.mark.django_db
class TestProfileUser:

    # тест атрибутов
    def test_view_class_attributes(self):
        assert ProfileUser.model == User
        assert ProfileUser.template_name == 'users/profile.html'
        assert ProfileUser.extra_context == {'title': "Профиль пользователя"}
        assert ProfileUser.form_class.__name__ == 'ProfileUserForm'

    # тест страницы профиля пользователя
    def test_profile_page(self, client, user):
        url = reverse('users:profile')

        # неавторизованный пользователь
        response = client.get(url)
        assert response.status_code == 302  # редирект на страницу входа
        assert reverse('users:login') in response.url

        client.force_login(user)

        # авторизованный пользователь
        get_response = client.get(url)
        assert get_response.status_code == 200
        assert get_response.context['title'] == "Профиль пользователя"
        assert 'users/profile.html' in [template.name for template in get_response.templates]


# тест страницы авторизации
@pytest.mark.django_db
class TestLoginUser:

    # тест атрибутов
    def test_view_class_attributes(self):
        assert LoginUser.form_class == AuthenticationForm
        assert LoginUser.template_name == 'users/login.html'
        assert LoginUser.extra_context == {'title': 'Авторизация'}

    # тест представления страницы
    def test_view_login_page(self, client):
        response = client.get(reverse('users:login'))
        assert response.status_code == 200
        assert response.context['title'] == 'Авторизация'
        assert isinstance(response.context['form'], AuthenticationForm)
        assert 'users/login.html' in [t.name for t in response.templates]

    # тест авторизации
    def test_successful_login(self, client, user):
        response = client.post(
            reverse('users:login'),
            {'username': 'Test_user', 'password': 'Password'}
        )
        assert response.status_code == 302
        assert response.url == '/'
        assert '_auth_user_id' in client.session

    # тест проверки данных
    @pytest.mark.parametrize("users, errors", [
        ({'username': 'Test_user', 'password': 'password'},
         'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'),
        ({'username': 'test_user', 'password': 'Password'},
         'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'),
        ({'password': 'Password'}, 'Обязательное поле'),
        ({'username': 'Test_user'}, 'Обязательное поле'),
    ])
    def test_login_errors(self, client, user, users, errors):
        response = client.post(reverse('users:login'),users)
        assert response.status_code == 200
        assert errors in response.content.decode()

    # тест CSRF-токена
    def test_csrf_token_in_form(self, client):
        response = client.get(reverse('users:login'))
        assert 'csrfmiddlewaretoken' in response.content.decode()


# тест страницы регистрации
@pytest.mark.django_db
class TestRegisterUser:

    # тест атрибутов
    def test_view_class_attributes(self):
        assert RegisterUser.form_class == RegisterUserForm
        assert RegisterUser.template_name == 'users/register.html'
        assert RegisterUser.extra_context == {'title': 'Регистрация'}
        assert RegisterUser.success_url == reverse_lazy('users:login')

    # тест представления страницы
    def test_view_register_page(self, client):
        response = client.get(reverse('users:register'))
        assert response.status_code == 200
        assert response.context['title'] == 'Регистрация'
        assert response.context['view'].success_url == '/users/login/'
        assert isinstance(response.context['form'], RegisterUserForm)
        assert response.template_name == ['users/register.html']

    # тест регистрации
    def test_register(self, client):
        response = client.post(
            reverse('users:register'),
            {'username': 'Test_user', 'password1': 'SecurePass123', 'password2': 'SecurePass123'}
        )
        assert response.status_code == 302
        assert response.url == '/users/login/'
        assert User.objects.count() == 1
        assert User.objects.get().username == 'Test_user'
        assert User.objects.get().password.startswith('pbkdf2')

    # тест CSRF - токена
    def test_csrf_token_in_form(self, client):
        response = client.get(reverse('users:register'))
        assert 'csrfmiddlewaretoken' in response.content.decode()

    # тест проверки данных
    @pytest.mark.parametrize("users, errors", [
        ({'username': 'Test_user', 'password': 'password'},
         'Пользователь с таким именем уже существует.'),
        ({'username': '   ', 'password': 'Password'},
         'Обязательное поле'),
        ({'password': 'Password'}, 'Обязательное поле'),
        ({'username': 'Test_user'}, 'Обязательное поле'),
    ])
    def test_register_errors(self, client, users, user, errors):
        response = client.post(reverse('users:register'),users)
        assert response.status_code == 200
        assert errors in response.content.decode()


# тест выхода из учётки
@pytest.mark.django_db
class TestLogoutUser:

    # тест выхода из учётки
    def test_logout(self, client, user):
        client.force_login(user)
        response = client.get(reverse('users:logout'))
        assert response.status_code == 302
        assert response.url == reverse('home')
        assert '_auth_user_id' not in client.session


# тест страницы изменения пароля
@pytest.mark.django_db
class TestUserPasswordChange:

    # тест атрибутов
    def test_view_class_attributes(self):
        assert UserPasswordChange.template_name == 'users/password_change.html'
        assert UserPasswordChange.extra_context == {'title': "Изменение пароля"}
        assert UserPasswordChange.form_class.__name__ == 'UserPasswordChangeForm'
        assert UserPasswordChange.success_url == reverse_lazy("users:password_change_done")

    # тест представления страницы
    def test_view_pas_change_page(self, client, user):
        client.force_login(user)
        response = client.get(reverse('users:password_change'))
        assert response.status_code == 200
        assert response.context['title'] == 'Изменение пароля'
        assert isinstance(response.context['form'], UserPasswordChangeForm)
        assert 'users/password_change.html' in [t.name for t in response.templates]

    # тест изменения пароля
    def test_pas_change(self, client, user):
        client.force_login(user)
        data = {'old_password': 'Password',
                'new_password1': 'NewSecurePass123!',
                'new_password2': 'NewSecurePass123!'}
        response = client.post(reverse('users:password_change'), data)
        user.refresh_from_db()
        assert user.check_password('NewSecurePass123!')
        assert response.status_code == 302
        assert response.url == '/users/password-change/done/'
        assert '_auth_user_id' in client.session

    # тест проверки вводимых паролей
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
    def test_password_valid(self, old_pass, new_pass1, new_pass2, errors, user, client):
        client.force_login(user)
        data = {
            'old_password': old_pass,
            'new_password1': new_pass1,
            'new_password2': new_pass2
        }
        response = client.post(reverse('users:password_change'), data)
        assert response.status_code == 200
        assert list(response.context['form'].errors.keys()) == errors

    # тест CSRF-токена
    def test_csrf_token_in_form(self, client, user):
        client.force_login(user)
        response = client.get(reverse('users:password_change'))
        assert 'csrfmiddlewaretoken' in response.content.decode()

    # тест страницы подтверждения изменения пароля
    def test_password_change_done(self, client, user):
        client.force_login(user)
        response = client.get(reverse('users:password_change_done'))
        assert response.status_code == 200
        assert response.context['view'].title == 'Пароль успешно изменен'
        assert response.template_name == ['users/password_change_done.html']