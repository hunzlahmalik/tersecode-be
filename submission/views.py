from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Submission


class SubmissionIndexView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'submission:submissions'
    login_url = 'account:login'

    def get_redirect_url(self):
        return reverse_lazy(self.pattern_name, kwargs={'slug': self.request.user.username})


class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'submission/list.html'
    context_object_name = 'submissions'
    slug_field = 'user__username'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return self.model.objects.filter(user__username=self.kwargs['slug'])


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = 'submission/detail.html'
    context_object_name = 'submission'
