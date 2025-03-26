from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView

from .forms import MeetingForm, CommentForm
from .models import Meeting


# создание встречи
class MeetingCreateView(LoginRequiredMixin, CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'meetings/suggest_an_appointment.html'
    success_url = reverse_lazy('check')

    # добавляем дополнительные данные в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Создание встречи"
        return context

    # добавляем автора и меняем на заглавную букву Повод для встречи
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.reason_to_meet = form.cleaned_data['reason_to_meet'].capitalize()
        return super().form_valid(form)


# изменение встречи
class UpdateMeeting(UpdateView):
    model = Meeting
    fields =['reason_to_meet', 'address', 'meeting_place', 'what_to_do', 'dress_code', 'link', 'date_meeting']
    template_name = 'meetings/suggest_an_appointment.html'
    success_url = reverse_lazy('check')


# удаление встречи
class DeleteMeeting(DeleteView):
    model = Meeting
    success_url = reverse_lazy('check')


# все встречи
@login_required
def view_meetings(request):
    meetings = Meeting.objects.all().order_by('date_meeting') # все встречи из базы
    paginator = Paginator(meetings, 4)  # пагинатор по 4 элемента на страницу
    page_number = request.GET.get('page', 1)  # номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number)   # объект страницы
    return render(request, 'meetings/check.html', {'page_obj': page_obj, 'title': "Все встречи",})


# детали встречи + комменты
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