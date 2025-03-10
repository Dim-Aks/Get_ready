from django.shortcuts import render, redirect
from django.views.generic import CreateView

#from get_ready.meetings.forms import MeetingForm
#from get_ready.meetings.models import Meeting


def index(requests):
    return render(requests, 'meetings/index.html')

def create_suggest(requests):
    # error = ''
    # if requests.method == 'POST':
    #     form = MeetingForm(requests.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
    #     else:
    #         error = 'Форма былa заполнена неверно'
    #
    # form = MeetingForm()
    # data ={'form': form,
    #        'error': error}
    return render(requests, 'meetings/suggest_an_appointment.html')

def check(requests):
    return render(requests, 'meetings/check.html')
