from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.models import CustomUser
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя',
    }




class RegisterView(TemplateView):
    template_name = 'authapp/register.html'
    extra_context = {
        'title': 'Резистрация пользователя',
    }

    def post(self, request, *args, **kwargs):
        try:
            if all(
                    (
                        request.POST.get('username'),
                        request.POST.get('email'),
                        request.POST.get('first_name'),
                        request.POST.get('last_name'),
                        request.POST.get('age'),
                        request.POST.get('password_1') == request.POST.get('password_2'),
                    )
            ):
                new_user = CustomUser.objects.create(
                    username=request.POST.get('username'),
                    email=request.POST.get('email'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    age=request.POST.get('age') if request.POST.get('age') else 0,
                    avatar=request.FILES.get('avatar'),
                )
                new_user.set_password(request.POST.get('password_1'))
                new_user.save()
                messages.add_message(request, messages.INFO, 'Регистрация завершена')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    'Что-то пошло не так'
                )
                return HttpResponseRedirect(reverse('authapp:register'))
        except Exception as ex:
            print(ex)
            messages.add_message(
                request,
                messages.WARNING,
                'Что-то пошло не так'
            )
            return HttpResponseRedirect(reverse('authapp:register'))


class CustomLogoutView(LogoutView):
    pass


class EditView(TemplateView):
    template_name = 'authapp/edit.html'
    extra_context = {
        'title': 'Резистрация пользователя',
    }

    def post(self, request, *args, **kwargs):
        if request.POST.get('username'):
            request.user.username = request.POST.get('username')

        if request.POST.get('fist_name'):
            request.user.fist_name = request.POST.get('fist_name')

        if request.POST.get('last_name'):
            request.user.last_name = request.POST.get('last_name')

        if request.POST.get('age'):
            request.user.age = request.POST.get('age')

        # if request.POST.get('password'):
        #     request.user.set_password(request.POST.get('password1'))

        request.user.save()
        return HttpResponseRedirect(reverse('authapp:edit'))
