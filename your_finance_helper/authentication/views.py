from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegisterForm, LoginUserForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            login(self.request, user)
            return redirect('main_page')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'authentication/login.html'


def logout_user(request):
    logout(request)
    return redirect('login')
