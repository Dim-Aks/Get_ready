import pytest
from django.urls import reverse

from .conftest import date_create_meet, past_meeting
from ..models import Meeting


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
    assert reverse('users:login') in response.url

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
    assert reverse('users:login') in response.url

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
    assert reverse('users:login') in response.url

    client.force_login(user)

    del_response = client.post(url)
    assert del_response.status_code == 302
    assert del_response.url == reverse('check')
    assert not Meeting.objects.filter(pk=meeting.pk)


# тест страницы всех встреч с пагинацей и фильтрацией
@pytest.mark.django_db
def test_meeting_list_view(client, user, meeting_factory):
    url = reverse('check')

    # создаем тестовые встречи
    meeting_factory.create_batch(3) # будущие встречи
    meeting_factory.create_batch(4, date_meeting= past_meeting) # прошедшие встречи
    meeting_factory.create_batch(2, author=user)  # встречи одного пользователя

    response = client.get(url)
    assert response.status_code == 302
    assert reverse('users:login') in response.url

    client.force_login(user)

    # все встречи (
    get_response_all = client.get(url, {'filter': 'all'})
    assert get_response_all.status_code == 200
    assert len(get_response_all.context_data['paginator'].object_list) == 9
    assert len(get_response_all.context['meetings']) == 4 # Проверка пагинации
    assert get_response_all.context['title'] == "Запланированные встречи"

    # будущие встречи
    get_response_actual = client.get(url, {'filter': 'actual'})
    assert get_response_actual.status_code == 200
    assert len(get_response_actual.context_data['paginator'].object_list) == 5
    assert len(get_response_actual.context['meetings']) == 4
    assert get_response_actual.context['title'] == "Запланированные встречи"

    # встречи пользователя
    get_response_author = client.get(url, {'filter': 'author'})
    assert get_response_author.status_code == 200
    assert len(get_response_author.context['meetings']) == 2
    assert get_response_author.context['title'] == "Запланированные встречи"

    # прошедшие встречи
    get_response_past = client.get(url, {'filter': 'past'})
    assert get_response_past.status_code == 200
    assert len(get_response_past.context['meetings']) == 4
    assert get_response_past.context['title'] == "Запланированные встречи"

# тест страницы деталей встреч + комменты
class TestMeetingDetail:
    # тест страницы деталей встреч
    @pytest.mark.django_db
    def test_meeting_detail(self, client, meeting, user):

        url = reverse('meeting_detail', kwargs={'pk': meeting.pk})

        response = client.post(url)
        assert response.status_code == 302
        assert reverse('users:login') in response.url

        client.force_login(user)

        get_response_404 = client.get(reverse('meeting_detail', kwargs={'pk': 5}))
        assert get_response_404.status_code == 404

        get_response = client.get(url)
        assert get_response.status_code == 200
        assert get_response.context['title'] == "Детали встречи"


    # тест комментов на странице деталей
    @pytest.mark.django_db
    def test_meeting_detail_comment(self, client, user, meeting):
        client.force_login(user)
        url = reverse('meeting_detail', kwargs={'pk': meeting.pk})

        # пустой коммент
        data_null = {'text': ''}
        response_null = client.post(url, data_null)
        assert response_null.status_code == 200
        assert 'form' in response_null.context
        assert response_null.context['form'].errors

        # тест коммент
        data = {'text': 'Test comment'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert meeting.comments.count() == 1
        assert meeting.comments.first().text == 'Test comment'
