from django.db import models

class Meeting(models.Model):
    reason_to_meet = models.CharField('Повод для встречи', max_length=150)
    meeting_place = models.CharField('Место сбора' ,max_length=255)
    address = models.CharField('Адрес', max_length=150)
    what_to_do = models.TextField('Чем займёмся')
    dress_code = models.CharField('Дресс-код', max_length=150)
    link = models.URLField('Ссылка на место, мероприятие', blank=True)
    date_meeting = models.DateField('Когда собираемся')
    date_create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.meeting_place

