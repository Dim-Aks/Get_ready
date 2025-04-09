from datetime import date
import pytest
from django.urls import reverse
from ..models import Meeting

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


# тест страницы изменения встречи
@pytest.mark.django_db
def test_meeting_update_view(client, user, meeting):
    url = reverse('edit_page', kwargs={'pk': meeting.pk})

    # Неавторизованный пользователь
    response = client.get(url)
    assert response.status_code == 302

    client.force_login(user)

    get_response = client.get(url)
    assert get_response.status_code == 200

    data = {
        'reason_to_meet': 'test update reason_to_meet',
        'address': 'test update address',
        'meeting_place': 'test update meeting_place',
        'what_to_do': 'test update what_to_do',
        'dress_code': 'test update dress_code',
        'date_meeting': date_create_meet,
    }
    post_response = client.post(url, data)
    meeting.refresh_from_db()
    assert post_response.status_code == 302
    assert post_response.url == reverse('check')
    assert meeting.reason_to_meet == 'test update reason_to_meet'
    assert meeting.meeting_place == 'test update meeting_place'
    assert meeting.address == 'test update address'
    assert meeting.what_to_do == 'test update what_to_do'
    assert meeting.dress_code == 'test update dress_code'
    assert meeting.date_meeting == date_create_meet


# тест страницы удаления встречи
@pytest.mark.django_db
def test_meeting_delete(client, meeting, user):
    url = reverse('meeting_delete', kwargs={'pk': meeting.pk})

    response = client.post(url)
    assert response.status_code == 302

    client.force_login(user)

    del_response = client.post(url)
    assert del_response.status_code == 302
    assert del_response.url == reverse('check')
    assert not Meeting.objects.filter(pk=meeting.pk)
