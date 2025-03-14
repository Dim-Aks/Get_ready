from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import MeetingForm
from .models import Meeting


def create_suggest(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.user = request.user if request.user.is_authenticated else None
            meeting.save()
            return redirect('check')
    else:
        form = MeetingForm()
    
    data ={'form': form}
    return render(request, 'meetings/suggest_an_appointment.html', data)

