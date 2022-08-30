from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import generic
from .models import Profile
from submissions.models import Submission


class UserIndexView(LoginRequiredMixin, generic.RedirectView):
    permanent = False
    query_string = True
    pattern_name = "uprofile:detail"
    login_url = "users:login"


class UserDetailView(generic.DetailView):
    model = Profile
    login_url = "users:login"

    template_name = "profile/detail.html"
    context_object_name = "uprofile"
    fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__username",
        "bio",
        "avatar",
        "github",
        "linkedin",
        "country",
    ]

    def setup(self, request, *args, **kwargs):
        kwargs[self.pk_url_kwarg] = request.user.id
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs, pk=self.object.user.id)
        context["title"] = "User Detail"
        context["submissions"] = Submission.objects.filter(
            user=self.object.user
        ).count()
        context["accepted_submissions"] = Submission.objects.filter(
            user=self.object.user, status=Status.ACCEPTED
        ).count()
        context["attempted_questions"] = (
            Submission.objects.filter(user=self.object.user)
            .values("problem")
            .annotate(Count("problem"))
            .count()
        )
        context["accepted_questions"] = (
            Submission.objects.filter(user=self.object.user, status=Status.ACCEPTED)
            .values("problem")
            .annotate(Count("problem"))
            .count()
        )
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Profile
    fields = "__all__"
    login_url = "users:login"
    template_name = "profile/update.html"

    context_object_name = "uprofile"

    # disable user field
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["user"].disabled = True
        return form

    def setup(self, request, *args, **kwargs):
        kwargs[self.pk_url_kwarg] = request.user.id
        super().setup(request, *args, **kwargs)

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse_lazy("uprofile:detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update User"
        return context
