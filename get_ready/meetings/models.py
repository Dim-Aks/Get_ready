from django.db import models
from django.contrib.auth.models import User

class Meeting(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason_to_meet = models.CharField('Повод для встречи', max_length=150)
    meeting_place = models.CharField('Место сбора' ,max_length=255)
    address = models.CharField('Адрес', max_length=150)
    what_to_do = models.TextField('Чем займёмся')
    dress_code = models.CharField('Дресс-код', max_length=150)
    link = models.URLField('Ссылка на место, мероприятие', blank=True)
    date_meeting = models.DateField('Когда собираемся (дд.мм.гггг)')
    date_create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.reason_to_meet


class Comment(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Комментарий")
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)