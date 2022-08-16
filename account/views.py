from django.views.generic import RedirectView, CreateView, FormView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Count

from .forms import CustomUserCreationForm, UserForm
from .models import User
from .constants import LOGIN_PATTERN, LOGIN_REVESE_URL
from submission.models import Submission, Status


class UserIndexView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'account:detail'
    login_url = LOGIN_PATTERN

    def get_redirect_url(self):
        return reverse_lazy(
            self.pattern_name, kwargs={
                'slug': self.request.user.username})


class UserDetailView(DetailView):
    model = User
    template_name = 'account/detail.html'
    context_object_name = 'user'
    fields = ['first_name', 'last_name', 'email', 'username', 'bio',
              'avatar', 'github', 'linkedin',
              'country']
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Detail'
        context['submissions'] = Submission.objects.filter(
            user=self.object).count()
        context['accepted_submissions'] = Submission.objects.filter(
            user=self.object, status=Status.ACCEPTED).count()
        context['attempted_questions'] = Submission.objects.filter(
            user=self.object).values('problem').annotate(
            Count('problem')).count()
        context['accepted_questions'] = Submission.objects.filter(
            user=self.object, status=Status.ACCEPTED).values('problem').annotate(
            Count('problem')).count()
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User

    login_url = LOGIN_PATTERN

    form_class = UserForm
    template_name = 'account/update.html'
    slug_field = 'username'

    context_object_name = 'user'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse_lazy(
            'account:detail', kwargs={
                'slug': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update User'
        return context


class CustomLoginView(LoginView, LoginRequiredMixin):
    template_name = 'account/login.html'
    success_url = 'account:index'
    login_url = LOGIN_PATTERN
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class CustomSignUpView(CreateView, FormView):
    template_name = 'account/signup.html'
    form_class = CustomUserCreationForm

    success_url = LOGIN_REVESE_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context


class CustomLogoutView(LogoutView):
    next_page = LOGIN_REVESE_URL

    def get_next_page(self):
        return reverse_lazy(self.next_page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Logout'
        return context
