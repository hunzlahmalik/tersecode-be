from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, RedirectView

from .models import Submission


class SubmissionIndexView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = "submissions:submissions"
    login_url = "users:login"

    def get_redirect_url(self):
        return reverse_lazy(
            self.pattern_name, kwargs={"slug": self.request.user.username}
        )


class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = "submissions/list.html"
    context_object_name = "submissions"
    slug_field = "user__username"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return self.model.objects.filter(user__username=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Submissions"
        return context


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "submissions/detail.html"
    context_object_name = "submissions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Submission Details"
        return context
