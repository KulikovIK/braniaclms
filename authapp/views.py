from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя',
    }


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mainapp:main_page')


class CustomLogoutView(LogoutView):
    pass


class EditView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm

    template_name = 'authapp/edit.html'

    # Защитный механизм от перехода по учеткам пользователей
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('authapp:edit', args=[self.request.user.pk])
