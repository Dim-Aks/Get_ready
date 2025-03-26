from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import MeetingForm, CommentForm
from .models import Meeting

@login_required
def create_suggest(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False) # Сохраняем форму без комита в БД
            meeting.author = request.user # Присваиваем автора
            meeting.reason_to_meet = meeting.reason_to_meet.capitalize()
            meeting.save()  # сохраняем в БД
            return redirect('check') # Перенаправляем на страницу с созданными встречами
    else:
        form = MeetingForm()
    
    data ={'form': form,
           'title': "Создание встречи",}
    return render(request, 'meetings/suggest_an_appointment.html', data)


class UpdateMeeting(UpdateView):
    model = Meeting
    fields =['reason_to_meet', 'address', 'meeting_place', 'what_to_do', 'dress_code', 'link', 'date_meeting']
    template_name = 'meetings/suggest_an_appointment.html'
    success_url = reverse_lazy('check')


@login_required
def view_meetings(request):
    meetings = Meeting.objects.all().order_by('date_meeting') # все встречи из базы
    paginator = Paginator(meetings, 4)  # пагинатор по 4 элемента на страницу
    page_number = request.GET.get('page', 1)  # номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number)   # объект страницы
    return render(request, 'meetings/check.html', {'page_obj': page_obj, 'title': "Все встречи",})

@login_required
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
        'form': form,
        'title': "Детали встречи",
    })