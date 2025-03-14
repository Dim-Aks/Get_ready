from django.forms import ModelForm, DateInput, Textarea, TextInput
from .models import Meeting

class MeetingForm(ModelForm):
    class Meta:
        model = Meeting # указываем модель с которой работаем
        fields =['reason_to_meet', 'address', 'meeting_place', 'what_to_do', 'dress_code', 'link', 'date_meeting'] # поля, которые должны быть выведены в формочки
        widgets = {
            'reason_to_meet': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вышла новая настолка'  # текст внутри поля формы
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
                'placeholder': 'Ну хотя бы пару дней на сборы, ну'
            }),
        }