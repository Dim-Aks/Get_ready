from .conftest import date_create_meet, past_meeting
import pytest
from django.forms import DateInput, TextInput, Textarea
from ..forms import MeetingForm, CommentForm
from ..models import Meeting, Comment


# тесты формы создания встречи
class TestMeetingForm:

    def test_form_meta(self):
        # проверка привязки к модели
        assert MeetingForm.Meta.model == Meeting

        # проверка списка полей
        field = [
            'reason_to_meet',
            'address',
            'meeting_place',
            'what_to_do',
            'dress_code',
            'link',
            'date_meeting'
        ]
        assert MeetingForm.Meta.fields == field

    # проверка виджетов
    def test_form_widgets(self):
        form = MeetingForm
        test_widgets = {
            'reason_to_meet': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вышла новая настолка'
            }),
            'address': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ул. Шоссе в Лаврики 59 к 1'
            }),
            'meeting_place': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Чудный дворец'
            }),
            'what_to_do': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ооо ну тут много чего можно написать:)',
                'rows': 4
            }),
            'dress_code': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Необычные носочки'
            }),
            'link': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заценить куда подписываемся вообще (необязательно)'
            }),
            'date_meeting': DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Ну хотя бы пару дней на сборы, ну'
            }),
        }

        for field_name, expected in test_widgets.items():
            assert form.Meta.widgets[field_name].attrs == expected.attrs
            assert form.Meta.widgets[field_name].__class__ == expected.__class__

    # проверка валидности формы
    def test_form_valid(self):
        # прошедшая дата
        form = MeetingForm(data={
            'date_meeting': past_meeting,
            'reason_to_meet': 'Test',
            'address': 'Test',
            'meeting_place': 'Test',
            'what_to_do': 'Test',
            'dress_code': 'Test'
        })
        assert not form.is_valid()
        assert 'date_meeting' in form.errors
        assert "Дата встречи не может быть в прошлом" in form.errors['date_meeting'][0]

        # актуальная дата
        form = MeetingForm(data={
            'date_meeting': date_create_meet,
            'reason_to_meet': 'test',
            'address': 'Test',
            'meeting_place': 'Test',
            'what_to_do': 'Test',
            'dress_code': 'Test'
        })
        assert form.is_valid()
        assert form.clean_date_capitalize() == 'Test'

    # тест сохранения данных формы
    @pytest.mark.django_db
    def test_form_save(self, user):
        form_data = {
            'reason_to_meet': 'Игра в Тестирование',
            'address': 'ул. Тестовая 15',
            'meeting_place': 'Кафе Тест',
            'what_to_do': 'Будем играть в настольные игры',
            'dress_code': 'Неформальный',
            'date_meeting': date_create_meet,
            'link': 'https://test.com'
        }
        form = MeetingForm(data=form_data)
        assert form.is_valid()

        # сохранение с привязкой к пользователю
        meeting = form.save(commit=False)
        meeting.author = user
        meeting.save()
        assert Meeting.objects.count() == 1
        meeting_test = Meeting.objects.first()
        assert meeting_test.reason_to_meet == 'Игра в Тестирование'
        assert meeting_test.address == 'ул. Тестовая 15'
        assert meeting_test.meeting_place == 'Кафе Тест'
        assert meeting_test.what_to_do == 'Будем играть в настольные игры'
        assert meeting_test.dress_code == 'Неформальный'
        assert meeting_test.date_meeting == date_create_meet
        assert meeting_test.link == 'https://test.com'


# тесты формы создания комментария к встрече
class TestCommentForm:

    def test_form_meta(self):
        # проверка привязки к модели
        assert CommentForm.Meta.model == Comment

        # проверка полей
        field = ('text',)
        assert CommentForm.Meta.fields == field

        # проверка виджетов
        widget = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ну что, собираемся?'
            })
        }
        assert CommentForm.Meta.widgets.__class__ == widget.__class__
        assert CommentForm.Meta.widgets['text'].attrs == widget['text'].attrs
        assert CommentForm.Meta.widgets['text'].attrs['class'] == 'form-control'
        assert CommentForm.Meta.widgets['text'].attrs['rows'] == 2
        assert CommentForm.Meta.widgets['text'].attrs['placeholder'] == 'Ну что, собираемся?'

    # проверка валидности формы
    @pytest.mark.parametrize('text,valid', [
        ('Valid comment', True),
        ('', False),  # пустой комментарий
        ('   ', False),  # пробелы не считаются за содержимое
        ('test' * 250, True),  # длинный комментарий
    ])
    @pytest.mark.django_db
    def test_form_valid(self, text, valid):
        form = CommentForm(data={'text': text})
        assert form.is_valid() == valid



