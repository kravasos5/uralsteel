import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from uralsteel.settings import MEDIA_ROOT
from visual.forms import ChangeEmployeeInfoForm
from visual.models import Employees


class Main(TemplateView):
    '''Представление главной страницы'''
    template_name = 'visual/main.html'

class Ladles(TemplateView):
    '''Представление страницы с ковшами'''
    template_name = 'visual/ladles.html'

class Cranes(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/cranes.html'

class AccessDenied(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/access_denied.html'

class Form(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'layouts/form.html'

##############################################################################
# Система разграничения доступа
class EmployeeProfile(LoginRequiredMixin, TemplateView):
    '''Профиль пользователя'''
    template_name = 'visual/profile.html'

class LoginView(LoginView):
    '''Вход в аккаунт'''
    template_name = 'visual/login.html'

    def get_success_url(self):
        return reverse_lazy('main')

class LogoutView(LoginRequiredMixin, LogoutView):
    '''Выход из аккаунта'''
    template_name = 'visual/main.html'

class ChangeEmployeeInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    '''Изменение данных пользователя'''
    model = Employees
    template_name = 'visual/change_employee_info.html'
    form_class = ChangeEmployeeInfoForm
    success_message = 'Данные изменены'

    def setup(self, request, *args, **kwargs):
        self.id = request.user.id
        self.slug = request.user.slug
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.id)

    def get_success_url(self):
        return reverse_lazy('visual:employee-profile', kwargs={'slug': self.slug})

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

# Сброс пароля
class PasswordReset(PasswordResetView):
    '''Представление сброса пароля'''
    template_name = 'visual/password_reset.html'
    html_email_template_name = 'email/reset_letter_body.html'
    email_template_name = 'email/reset_letter_body.txt'
    subject_template_name = 'email/reset_letter_subject.txt'
    success_url = reverse_lazy('visual:password-reset-starting')

class PasswordResetStarting(PasswordResetDoneView):
    '''Оповещение о отправленном письме'''
    template_name = 'visual/password_reset_starting.html'

class PasswordResetConfrim(PasswordResetConfirmView):
    '''Представление подтверждения сброса пароля (ввод нового пароля)'''
    template_name = 'visual/password_reset_confirm.html'
    success_url = reverse_lazy('visual:password-reset-complete')

class PasswordResetComplete(PasswordResetCompleteView):
    '''Пароль успешно сброшен'''
    template_name = 'visual/password_reset_complete.html'
