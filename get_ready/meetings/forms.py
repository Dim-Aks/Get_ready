from django.utils import timezone

from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, Textarea, TextInput
from .models import Meeting, Comment


# форма создания встречи
class MeetingForm(ModelForm):
    class Meta:
        model = Meeting  # указываем модель с которой работаем
        fields = [
            "reason_to_meet",
            "address",
            "meeting_place",
            "what_to_do",
            "dress_code",
            "link",
            "date_meeting",
        ]  # поля, которые должны быть выведены в формочки
        widgets = {
            "reason_to_meet": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Вышла новая настолка",  # текст внутри поля формы
                }
            ),
            "address": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ул. Шоссе в Лаврики 59 к 1",
                }
            ),
            "meeting_place": TextInput(
                attrs={"class": "form-control", "placeholder": "Чудный дворец"}
            ),
            "what_to_do": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ооо ну тут много чего можно написать:)",
                    "rows": 4,
                }
            ),
            "dress_code": TextInput(
                attrs={"class": "form-control", "placeholder": "Необычные носочки"}
            ),
            "link": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Заценить куда подписываемся вообще (необязательно)",
                }
            ),
            "date_meeting": DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Ну хотя бы пару дней на сборы, ну",
                }
            ),
        }

    # проверка даты, чтобы была не из прошлого
    def clean_date_meeting(self):
        date_meeting = self.cleaned_data.get("date_meeting")
        if date_meeting < timezone.now().date():
            raise ValidationError("Дата встречи не может быть в прошлом")
        return date_meeting

    # на заглавную букву Повод для встречи
    def clean_date_capitalize(self):
        reason_to_meet = self.cleaned_data.get("reason_to_meet")
        return reason_to_meet.capitalize()


# форма создания комментария в деталях встречи
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Ну что, собираемся?",
                }
            )
        }
