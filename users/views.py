from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    FormView,
)

from .forms import CustomUserCreationForm


class CustomLoginView(LoginView, LoginRequiredMixin):
    template_name = "users/login.html"
    success_url = "uprofile:detail"
    login_url = "users:login"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class CustomSignUpView(CreateView, FormView):
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = "uprofile:detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sign Up"
        return context


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")

    def get_next_page(self):
        return reverse_lazy(self.next_page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Logout"
        return context
