from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView

from visual.forms import ChangeEmployeeInfoForm, CranesAccidentForm, LadlesAccidentForm, AggregatAccidentForm, \
    LadlesAccidentDetailForm, CranesAccidentDetailForm, AggregatAccidentDetailForm, AccidentStartingForm
from visual.models import Employees, CranesAccident, LadlesAccident, AggregatAccident, Ladles, Cranes, Aggregates


class MainView(TemplateView):
    '''Представление главной страницы'''
    template_name = 'visual/main.html'

class LadlesView(TemplateView):
    '''Представление страницы с ковшами'''
    template_name = 'visual/ladles.html'

    def post(self, request, *args, **kwargs):
        '''Обработка post-запроса'''
        # получение времени
        time = request.POST.get('time')
        print(time)
        # формирование ответа
        data: dict = {'answer': 'received'}
        return JsonResponse(data=data, status=200)

class CranesView(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/cranes.html'

    def post(self, request, *args, **kwargs):
        '''Обработка post-запроса'''
        # формирование ответа
        data: dict = {'answer': 'received'}
        return JsonResponse(data=data, status=200)

class AccessDeniedView(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/access_denied.html'

##############################################################################
# Проишествия

class AccidentStartingView(TemplateView):
    '''Представление начала отчёта об аварии/проишествии'''
    template_name = 'visual/accident_starting.html'

    def get(self, request, *args, **kwargs):
        '''Вывод формы'''
        context = super().get_context_data(*args, **kwargs)
        form = AccidentStartingForm()
        context['form'] = form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        '''Обработка ответа формы'''
        form = AccidentStartingForm(request.POST)
        if form.is_valid():
            # получаю тип поломанного объекта (кран, ковш или агрегат)
            accident_type = form.cleaned_data['accident_type']
            # в зависимости от типа объекта возвращаю соответствующую страницу
            if accident_type == 'cr':
                # краны
                return HttpResponseRedirect(reverse('accident-crane'))
            elif accident_type == 'la':
                # ковши
                return HttpResponseRedirect(reverse('accident-ladle'))
            elif accident_type == 'ag':
                # агрегаты
                return HttpResponseRedirect(reverse('accident-aggregate'))
        else:
            return render(request, self.template_name, context={'form': form})

class AccidentViewBase(CreateView):
    '''Представление страницы с проишествиями'''
    template_name = 'visual/accident.html'
    # необходимо задать form_class, model, check_model
    # (check_model нужна для проверки зарегистрирована ли в бд такая поломка)
    # success_url
    # также необходимо определить метод form_invalid, вызывающий
    # исключение, если предмет жалобы уже отмечен, как неисправный

    def is_exists(self, instance):
        # Проверяет зарегистрирована ли такая поломка
        if self.check_model.objects.filter(id=instance.object.id, is_broken=True).exists():
            return True
        return False

    def form_invalid(self, form, *args, **kwargs):
        # Если такая поломка зарегистрирована
        if kwargs.get('is_exist'):
            form.add_error(None, 'Этот объект уже отмечен, как сломанный')
        else:
            form.add_error(None, 'Ошибка при отправке отчёта')
        return super().form_invalid(form)

    def form_valid(self, form, *args, **kwargs):
        # задаю автора отчёта
        form.instance.author = self.request.user
        # проверка не зарегистрирована ли такая поломка
        if self.is_exists(form.instance):
            return self.form_invalid(form, is_exist=True, *args, **kwargs)
        try:
            return super().form_valid(form)
        except IntegrityError:
            return self.form_invalid(form, *args, **kwargs)

class AccidentDetailStartingViewBase(TemplateView):
    '''
    Представление детального комментария отчёта об аварии/поломке
    Метод get_success_url нужно переопределить, а метод get_context_data
    расширить
    '''
    template_name = 'visual/accident_detail_starting.html'

class AccidentDetailViewBase(UpdateView):
    '''Представление страницы с формой заполнения подробного описания проишествия'''
    template_name = 'visual/accident_detail.html'
    success_url = reverse_lazy('main')
    # необходимо задать form_class, model

class LadleAccidentView(AccidentViewBase):
    '''Представление обработчик проишествия ковша'''
    form_class = LadlesAccidentForm
    model = LadlesAccident
    check_model = Ladles

    def get_success_url(self, *agrs, **kwargs):
        return reverse_lazy('accident-ladle-detail-starting', kwargs={'pk': self.object.id})

class LadleAccidentDetailStartingView(AccidentDetailStartingViewBase):
    '''
    Представление начала написания дополнительного
    комментария при проишествии с ковшом
    '''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        url = reverse('accident-ladle-detail', kwargs={'pk': kwargs.get('pk')})
        context['detail_url'] = url
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('accident-ladle-detail', kwargs={'pk': kwargs.get('pk')})

class LadleAccidentDetailView(AccidentDetailViewBase):
    '''
    Представление обработчик написания дополнительного
    комментария при проишествии с ковшом
    '''
    form_class = LadlesAccidentDetailForm
    model = LadlesAccident

class CraneAccidentView(AccidentViewBase):
    '''Представление обработчик проишествия крана'''
    form_class = CranesAccidentForm
    model = CranesAccident
    check_model = Cranes

    def get_success_url(self, *agrs, **kwargs):
        return reverse_lazy('accident-crane-detail-starting', kwargs={'pk': self.object.id})

class CraneAccidentDetailStartingView(AccidentDetailStartingViewBase):
    '''
    Представление начала написания дополнительного
    комментария при проишествии с краном
    '''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        url = reverse('accident-crane-detail', kwargs={'pk': kwargs.get('pk')})
        context['detail_url'] = url
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('accident-crane-detail', kwargs={'pk': kwargs.get('pk')})

class CraneAccidentDetailView(AccidentDetailViewBase):
    '''
    Представление обработчик написания дополнительного
    комментария при проишествии с краном
    '''
    form_class = CranesAccidentDetailForm
    model = CranesAccident

class AggregateAccidentView(AccidentViewBase):
    '''Представление обработчик проишествия агрегата'''
    form_class = AggregatAccidentForm
    model = AggregatAccident
    check_model = Aggregates

    def get_success_url(self, *agrs, **kwargs):
        return reverse_lazy('accident-aggregate-detail-starting', kwargs={'pk': self.object.id})

class AggregateAccidentDetailStartingView(AccidentDetailStartingViewBase):
    '''
    Представление начала написания дополнительного
    комментария при проишествии с агрегатом
    '''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        url = reverse('accident-aggregate-detail', kwargs={'pk': kwargs.get('pk')})
        context['detail_url'] = url
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('accident-aggregate-detail', kwargs={'pk': kwargs.get('pk')})

class AggregateAccidentDetailView(AccidentDetailViewBase):
    '''
    Представление обработчик написания дополнительного
    комментария при проишествии с агрегатом
    '''
    form_class = AggregatAccidentDetailForm
    model = AggregatAccident

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
