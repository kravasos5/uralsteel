from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from visual.forms import ChangeEmployeeInfoForm
from visual.models import Employees


class MainView(TemplateView):
    '''Представление главной страницы'''
    template_name = 'visual/main.html'

class LadlesView(TemplateView):
    '''Представление страницы с ковшами'''
    template_name = 'visual/ladles.html'

class CranesView(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/cranes.html'

class AccessDeniedView(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/access_denied.html'

class AccidentView(TemplateView):
    '''Представление страницы с проишествиями'''
    template_name = 'visual/accident.html'

##############################################################################
# Система разграничения доступа
class EmployeeProfile(LoginRequiredMixin, TemplateView):
    '''Профиль пользователя'''
    template_name = 'visual/profile.html'

class EmployeeLoginView(LoginView):
    '''Вход в аккаунт'''
    template_name = 'visual/login.html'

    def get_success_url(self):
        return reverse_lazy('main')

class EmployeeLogoutView(LoginRequiredMixin, LogoutView):
    '''Выход из аккаунта'''
    template_name = 'visual/main.html'

class ChangeEmployeeInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView): #
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
        return reverse_lazy('profile', kwargs={'slug': self.slug})

    def form_valid(self, form):
        super().form_valid(form)
        # проверяю добавил ли пользователь новое фото, если да, то
        # is_crop_photo = True
        is_crop_photo = str(form.cleaned_data.get('photo')) == 'photo.png'
        # и если пользователь добавил фото, то отправляю ссылку для перехода
        if is_crop_photo:
            return JsonResponse(data={'url': self.get_success_url()}, status=200)
        # если пользователь не добавлял новое фото, то отправляется
        # стандартный ответ
        return HttpResponseRedirect(self.get_success_url())

# Сброс пароля
class PasswordReset(PasswordResetView):
    '''Представление сброса пароля'''
    template_name = 'visual/password_reset.html'
    html_email_template_name = 'email/reset_letter_body.html'
    email_template_name = 'email/reset_letter_body.txt'
    subject_template_name = 'email/reset_letter_subject.txt'
    success_url = reverse_lazy('pass-reset-starting')

class PasswordResetStarting(PasswordResetDoneView):
    '''Оповещение о отправленном письме'''
    template_name = 'visual/password_reset_starting.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    '''Представление подтверждения сброса пароля (ввод нового пароля)'''
    template_name = 'visual/password_reset_confirm.html'
    success_url = reverse_lazy('pass-reset-complete')

class PasswordResetComplete(PasswordResetCompleteView):
    '''Пароль успешно сброшен'''
    template_name = 'visual/password_reset_complete.html'
