from datetime import date

import pytest
from django.urls import reverse

date_create_meet = date(2026,4,8)

# тест отображения домашней страницы
def test_home_page(client):
    url = reverse('home')
    response = client.get(url)

    assert response.status_code == 200
    assert 'Собирайся!' in response.context_data['title']


# тест страницы создания встречи
@pytest.mark.django_db
def test_meeting_create_view(client, user):
    url = reverse('suggest')

    # Неавторизованный пользователь
    response = client.get(url)
    assert response.status_code == 302 # Редирект на страницу входа

    # типо залогинился
    client.force_login(user)

    # GET-запрос
    get_response = client.get(url)
    assert get_response.status_code == 200
    assert get_response.context['title'] == "Создание встречи"

    # POST-запрос с валидными данными
    data = {
        'reason_to_meet': 'test reason_to_meet',
        'address': 'test address',
        'meeting_place': 'test meeting_place',
        'what_to_do': 'test what_to_do',
        'dress_code': 'test dress_code',
        'date_meeting': date_create_meet,
    }
    post_response = client.post(url, data)
    assert post_response.status_code == 302
    assert post_response.url == reverse('check')

