from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, CreateView, DeleteView, ListView

from .forms import MeetingForm, CommentForm
from .models import Meeting


# создание встречи
class MeetingCreateView(LoginRequiredMixin, CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = "meetings/suggest_an_appointment.html"
    success_url = reverse_lazy("check")

    # добавляем дополнительные данные в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание встречи"
        return context

    # добавляем автора для встречи
    def form_valid(self, form):
        form.instance.author = self.request.user
        # form.instance.reason_to_meet = form.cleaned_data['reason_to_meet'].capitalize()
        return super().form_valid(form)


# изменение встречи
class UpdateMeeting(LoginRequiredMixin, UpdateView):
    model = Meeting
    fields = [
        "reason_to_meet",
        "address",
        "meeting_place",
        "what_to_do",
        "dress_code",
        "link",
        "date_meeting",
    ]
    template_name = "meetings/suggest_an_appointment.html"
    success_url = reverse_lazy("check")


# удаление встречи
class DeleteMeeting(LoginRequiredMixin, DeleteView):
    model = Meeting
    success_url = reverse_lazy("check")


# все встречи
class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = "meetings/check.html"
    context_object_name = "meetings"
    paginate_by = 4

    # фильтрация встреч
    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.GET.get("filter", "actual")
        now = timezone.now()

        if filter_type == "author":
            queryset = queryset.filter(author=self.request.user)
        elif filter_type == "past":
            queryset = queryset.filter(date_meeting__lt=now)
        elif filter_type == "all":
            pass
        else:
            queryset = queryset.filter(date_meeting__gte=now)

        return queryset.order_by("date_meeting")

    # добавляем дополнительные данные в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запланированные встречи"
        context["current_filter"] = self.request.GET.get("filter", "actual")
        return context


# детали встречи + комменты
@login_required
def meeting_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    comments = meeting.comments.all().order_by("-created_date")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.meeting = meeting
            comment.author = request.user
            comment.save()
            return redirect("meeting_detail", pk=pk)
    else:
        form = CommentForm()

    return render(
        request,
        "meetings/meeting_detail.html",
        {
            "meeting": meeting,
            "comments": comments,
            "form": form,
            "title": "Детали встречи",
        },
    )
