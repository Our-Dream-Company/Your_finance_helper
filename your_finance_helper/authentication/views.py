from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import request
from django.shortcuts import redirect
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegisterForm, LoginUserForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form_class):
        valid = super().form_valid(form_class)
        login(self.request, self.object)
        return valid


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'authentication/login.html'


def logout_user(request):
    logout(request)
    return redirect('login')
