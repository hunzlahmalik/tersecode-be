from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from submission.models import Submission, Status
from .models import Solution, Problem
from .forms import SolutionForm


class ProblemDetailView(generic.DetailView):
    model = Problem
    template_name = 'problem/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Problem Detail'
        context['statement'] = self.object.statement.read().decode('utf-8')
        return context


class ProblemListView(generic.ListView):
    model = Problem
    template_name = 'problem/list.html'
    context_object_name = 'problems'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Problems"
        for problem in context['problems']:
            problem.solved = Submission.objects.filter(
                problem=problem, status=Status.ACCEPTED).count() > 0
        return context


class SolutionView(generic.DetailView):
    model = Problem
    template_name = 'problem/solution.html'
    context_object_name = 'problem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Solution'
        context['solution'] = self.object.solution.solution.read().decode('utf-8')
        return context


class SubmissionView(LoginRequiredMixin, generic.CreateView):
    template_name = 'problem/submit.html'
    model = Submission
    fields = ['language', 'code']
    login_url = reverse_lazy('account:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Submit Your Solution'
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('submission:list')

    # before save
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.problem = get_object_or_404(
            Problem, id=self.kwargs['problem_id'])
        return super().form_valid(form)
