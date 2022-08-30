from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from submissions.models import Submission
from .models import Problem


class ProblemDetailView(generic.DetailView):
    model = Problem
    template_name = "problems/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Problem Detail"
        context["statement"] = self.object.statement.read().decode("utf-8")
        return context


class ProblemListView(generic.ListView):
    model = Problem
    template_name = "problems/list.html"
    context_object_name = "problems"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Problems"
        for problem in context["problems"]:
            problem.solved = (
                Submission.objects.filter(
                    problem=problem, status=Submission.Status.ACCEPTED
                ).count()
                > 0
            )
        return context


class SolutionView(generic.DetailView):
    model = Problem
    template_name = "problems/solution.html"
    context_object_name = "problems"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Solution"
        context["solution"] = self.object.solution.solution.read().decode("utf-8")
        return context


class SubmissionView(LoginRequiredMixin, generic.CreateView):
    template_name = "problems/submit.html"
    model = Submission
    fields = ["language", "code"]
    login_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Submit Your Solution"
        return context

    def get_success_url(self) -> str:
        return reverse_lazy("submissions:list")

    # before save
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.problem = get_object_or_404(Problem, id=self.kwargs["problem_id"])
        return super().form_valid(form)
