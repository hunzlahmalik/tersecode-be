from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from submission.models import Submission
from .models import Solution, Problem
from .forms import SolutionForm


class ProblemDetailView(generic.DetailView):
    model = Problem
    template_name = 'problem/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SolutionForm(
            initial={'problem': self.object})
        context['statement'] = self.object.statement.read().decode('utf-8')
        return context


class ProblemListView(generic.ListView):
    model = Problem
    template_name = 'problem/list.html'
    context_object_name = 'problems'


class SolutionView(generic.FormView):
    template_name = 'problem/solution.html'
    form_class = SolutionForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problem'] = get_object_or_404(
            Problem, id=self.kwargs['problem_id'])
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('problem:detail',
                                            args=(self.kwargs['problem_id'],)))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['problem'] = get_object_or_404(
            Problem, id=self.kwargs['problem_id'])
        return kwargs

# Create Submission Form View


class SubmissionView(generic.CreateView):
    template_name = 'problem/submit.html'
    model = Submission
    fields = ['language', 'code']

    def get_success_url(self) -> str:
        return reverse_lazy('submission:list')

    # before save
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.problem = get_object_or_404(
            Problem, id=self.kwargs['problem_id'])
        return super().form_valid(form)
