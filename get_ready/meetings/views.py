from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MeetingForm, CommentForm
from .models import Meeting

@login_required
def create_suggest(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False) # Сохраняем форму без коммита в БД
            meeting.author = request.user # Присваиваем автора
            meeting.save()  # Теперь сохраняем в БД
            return redirect('check') # Перенаправляем на страницу с созданными встречами
    else:
        form = MeetingForm()
    
    data ={'form': form}
    return render(request, 'meetings/suggest_an_appointment.html', data)

@login_required
def view_meetings(request):
    meetings = Meeting.objects.all().order_by('date_meeting')
    return render(request, 'meetings/check.html', {'meetings': meetings})

def meeting_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    comments = meeting.comments.all().order_by('-created_date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.meeting = meeting
            comment.author = request.user
            comment.save()
            return redirect('meeting_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'meetings/meeting_detail.html', {
        'meeting': meeting,
        'comments': comments,
        'form': form
    })
