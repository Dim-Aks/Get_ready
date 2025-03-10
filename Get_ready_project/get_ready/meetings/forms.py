# from django.forms import ModelForm, DateInput, Textarea, TextInput
#
# from get_ready.meetings.models import Meeting
#
# class MeetingForm(ModelForm):
#     model = Meeting # указываем модель с которой работаем
#     fields =['meeting_place', 'what_to_do', 'link', 'date_meeting'] # поля, которые должны быть выведены в формочки
#     widgets = {
#         'meeting_place': TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Где собираемся'
#         }),
#         'what_to_do': TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Чем займёмся'
#         }),
#         'link': Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Ссылка на место/ мероприятие'
#         }),
#         'date_meeting': DateInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Когда собираемся'
#         }),
#     }