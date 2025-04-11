import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from ..views import ProfileUser


# тестовый пользователь
@pytest.fixture()
def user():
    return User.objects.create_user(
        username='Test_user',
        email='Test@mail.com',
        password='Password')


# тест профиля пользователя
class TestProfileUser:

    # тест аттрибутов
    def test_view_class_attributes(self):
        assert ProfileUser.model == User
        assert ProfileUser.template_name == 'users/profile.html'
        assert ProfileUser.extra_context == {'title': "Профиль пользователя"}
        assert ProfileUser.form_class.__name__ == 'ProfileUserForm'

    # тест страницы профиля пользователя
    @pytest.mark.django_db
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
