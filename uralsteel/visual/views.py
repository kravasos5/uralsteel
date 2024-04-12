import datetime, os, json
from typing import List, Type, Optional

import glob2
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, UpdateView, CreateView

from visual.forms import ChangeEmployeeInfoForm, CranesAccidentForm, LadlesAccidentForm, AggregatAccidentForm, \
    LadlesAccidentDetailForm, CranesAccidentDetailForm, AggregatAccidentDetailForm, AccidentStartingForm
from visual.mixins import RedisCacheMixin
from visual.models import Employees, CranesAccident, LadlesAccident, AggregatAccident, Ladles, Cranes, Aggregates, \
    ActiveDynamicTable, ArchiveDynamicTable


class MainView(TemplateView):
    '''Представление главной страницы'''
    template_name = 'visual/main.html'

class LadlesView(TemplateView):
    '''Представление страницы с ковшами'''
    template_name = 'visual/ladles.html'
    def get(self, request, *args, **kwargs):
        '''Обработка get-запроса'''
        context = {}
        # проверяю нет ли в redis ключа-времени
        result: str = LadlesView.get_key_redis('ltimeform')
        if result is not None:
            context['timeformvalue'] = result
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        '''Обработка post-запроса'''
        if request.POST.get('operation_id'):
            # если запрос диспетчера, то есть подтвердили перемещение
            # ковша или начало операции или подтвердили завершение операции
            # получаю id объекта модели ActiveDynamicTable
            operation_id: int = int(request.POST.get('operation_id'))
            # получаю тип операции
            operation_type: str = str(request.POST.get('operation_type'))
            # получаю объект операции или 404
            operation = get_object_or_404(ActiveDynamicTable, id=operation_id)
            # получаю время
            time = LadlesView.time_convert(request.POST.get('time'))
            # удаляю старые ключи из хранилища redis
            LadlesView.delete_keyy_redis('*ltime:*')
            status: int = 200
            match operation_type:
                case 'transporting':
                    # если ковш "транспортируемый"
                    # перезаписываю запись в архивную таблицу
                    LadlesView.from_active_to_archive(operation)
                    data: dict = {'st': 'перемещён в архив'}
                case 'starting':
                    # если ковш "начинающий"
                    # перезаписываю дату в операции Активной Таблицы,
                    # то есть теперь ковш стаёт "ожидающим"
                    operation.actual_start = time
                    operation.save()
                    data: dict = {'st': 'теперь ковш ожидающим'}
                case 'ending':
                    # если ковш "ожидающий"
                    # перезаписываю дату в операции Активной Таблицы,
                    # то есть теперь ковш стаёт "транспортируемым"
                    operation.actual_end = time
                    operation.save()
                    data: dict = {'st': 'теперь ковш транспортируемый'}
                case _:
                    # в таком случае status=400, то есть пользователь
                    # клиент неверно указал operation_type
                    data: dict = {'st': 'неверно указан operation_type'}
                    status: int = 400
        else:
            # если нужно отобразить ковши
            # получение времени
            date = LadlesView.time_convert(request.POST.get('time'))
            # получаю ковши и формирую ответ
            data: dict = LadlesView.get_ladles_info(date)
            status: int = 200
        return JsonResponse(data=data, status=status)

    @staticmethod
    def time_convert(time: str) -> datetime:
        '''Метод, переводящий время в удобный формат'''
        t: List[str, str] = time.split(':')
        hours: int = int(t[0])
        minutes: int = int(t[1])
        # записываю время в redis-cache
        LadlesView.set_key_redis('ltimeform', f'{hours}:{minutes}', 120)
        # получаю "наивную дату"
        naive_datetime = datetime.datetime(2023, 12, 11, hours, minutes)
        # преобразую её в "осведомлённую", то есть знающую часовой пояс
        aware_datetime = timezone.make_aware(naive_datetime, timezone.get_default_timezone())
        ############
        # в будущем здесь может быть любая дата, но будет текущий день
        # получаю текущий часовой пояс
        # current_timezone = pytz.timezone(TIME_ZONE)
        # получаю сегодняшнюю дату
        # today = timezone.now().astimezone(current_timezone)
        ############
        return aware_datetime

    @staticmethod
    def get_ladles_info(date: datetime) -> dict:
        '''Функция, извлекающая из БД информацию по положениям ковшей'''
        ladles_info: dict = {}
        # получаю все ковши, находящиеся в цеху в момент времени date
        # использую select_related, чтобы получить сразу в одном запросе
        # всю нужную информацию, по ковшу, по марке стали, по агрегату
        # На мнемосхеме будет отображаться "3 типа ковшей".
        # 1) Первый тип - "начинающий" операцию ковш,
        # у которого actual_start == null,
        # при этом предыдущая операция уже перенесена в архивную таблицу.
        # Такой ковш будет отображаться заштрихованным и только после
        # подтверждения начала операции диспетчером он станет
        # "ожидающим" ковшом.
        # 2) "Ожидающий" завершение операции ковш - ковш,
        # у которого actual_end == null,
        # то есть текущая операция не завершена, когда диспетчер отметит
        # что текущая операция завершена, то в БД автоматически запишется
        # actual_end и ковш перейдёт в состояние "транспортируемого".
        # 3) "Транспортируемый ковш" - ковш у которого actual_start
        # и actual_end == null. Этот ковш сейчас транспортируется
        # на следующую позицию и как только диспетчер подтвердит, что
        # ковш приехал, то текущая запись перенесётся в архивную таблицу,
        # а из активной будет удалена
        # Извлекаю "транспортируемые" ковши
        # получаю имя ключа, которое используется при кэшировании
        key_name: str = f"ltime:{date.strftime('%H-%M')}"
        # проверка наличия ключа в redis-cache
        result: Optional[dict] = LadlesView.get_key_redis_json(key_name)
        if result is not None:
            return result
        # если ключа нет, то брать информацию из базы данных,
        # она автоматически добавится в кэш в конце этого метода, перед return
        ladles_queryset = ActiveDynamicTable.objects \
            .select_related('ladle', 'brand_steel', 'aggregate') \
            .filter(actual_start__isnull=False, actual_end__isnull=False,
                    actual_start__lte=date)
                    # actual_start__lte=date, actual_end__gte=date)
        # добавляю всю нужную информацию в словарь
        ladles_info = LadlesView.cranes_into_dict(ladles_queryset, ladles_info, is_transporting=True)
        # Извлекаю "ожидающие" ковши
        ladles_queryset = ActiveDynamicTable.objects \
            .select_related('ladle', 'brand_steel', 'aggregate') \
            .filter(actual_start__isnull=False, actual_end__isnull=True,
                    actual_start__lte=date)
        # добавляю всю нужную информацию в словарь
        ladles_info = LadlesView.cranes_into_dict(ladles_queryset, ladles_info)
        # Извлекаю "начинающие" ковши
        ladles_queryset = ActiveDynamicTable.objects \
            .select_related('ladle', 'brand_steel', 'aggregate') \
            .filter(actual_start__isnull=True, actual_end__isnull=True,
                    plan_start__lt=date, plan_end__gt=date)
        # добавляю всю нужную информацию в словарь
        ladles_info = LadlesView.cranes_into_dict(ladles_queryset, ladles_info, is_plan=True)
        # добавление ключа в redis
        LadlesView.set_key_redis_json(key_name, ladles_info, 300)
        return ladles_info

    @staticmethod
    def cranes_into_dict(ladles_queryset, ladles_info: dict, is_transporting:bool=False, is_plan:bool=False) -> dict:
        '''
        Метод, преобразующий queryset ковшей в dict.
        Этот метод создаёт единый фундамент для всех видов
        ковшей, передаваемых фронту.
        '''
        for elem in ladles_queryset:
            if str(elem.ladle.id) in ladles_info:
                continue
            ladles_info[f'{elem.ladle.id}'] = {
                'ladle_title': f'{elem.ladle.title}',
                'x': elem.aggregate.coord_x,
                'y': elem.aggregate.coord_y,
                'num_melt': f'{elem.num_melt}',
                'brand_steel': f'{elem.brand_steel.title}',
                'aggregate': f'{elem.aggregate.title}',
                'plan_start': f'{elem.plan_start.astimezone(timezone.get_default_timezone())}',
                'plan_end': f'{elem.plan_end.astimezone(timezone.get_default_timezone())}',
                'next_aggregate': '-',
                'next_plan_start': '-',
                'next_plan_end': '-',
                'operation_id': elem.id
            }
            if is_transporting:
                # если ковш едет на следующую позицию, то есть
                # он "транспортируемый", то is_transporting=True
                ladles_info[f'{elem.ladle.id}']['is_transporting'] = True
            else:
                ladles_info[f'{elem.ladle.id}']['is_transporting'] = False

            if is_plan:
                # для "начинающих" ковшей
                ladles_info[f'{elem.ladle.id}']['photo'] = '/media/photos/aggregates/starting_ladle.png'
                ladles_info[f'{elem.ladle.id}']['is_starting'] = True
            else:
                # для "транспортируемых" и "ожидающих"
                ladles_info[f'{elem.ladle.id}']['photo'] = f'{elem.aggregate.photo.url}'
                ladles_info[f'{elem.ladle.id}']['is_starting'] = False

            # нахожу следующую позицию текущего ковша в БД
            next_elems = ActiveDynamicTable.objects \
                .select_related('aggregate') \
                .filter(ladle=elem.ladle, route=elem.route,
                        brand_steel=elem.brand_steel,
                        num_melt=elem.num_melt,
                        plan_start__gt=elem.plan_end) \
                .order_by('plan_start')
            # если следующая позиция присутствует, то обновляю
            # соответствующие поля словаря
            if next_elems.exists():
                # получаю следующую позицию ковша
                # это первый элемент next_elems, так как next_elems
                # отсортирован по plan_start
                next_elem = next_elems[0]
                ladles_info[f'{elem.ladle.id}']['next_aggregate'] = f'{next_elem.aggregate.title}'
                ladles_info[f'{elem.ladle.id}']['next_plan_start'] = f'{next_elem.plan_start.astimezone(timezone.get_default_timezone())}'
                ladles_info[f'{elem.ladle.id}']['next_plan_end'] = f'{next_elem.plan_end.astimezone(timezone.get_default_timezone())}'
                ladles_info[f'{elem.ladle.id}']['next_x'] = next_elem.aggregate.coord_x
                ladles_info[f'{elem.ladle.id}']['next_y'] = next_elem.aggregate.coord_y
                ladles_info[f'{elem.ladle.id}']['next_id'] = next_elem.id
            elif next_elems.exists() == False and ladles_info[str(elem.ladle.id)]['is_transporting'] == True:
                # если ковш отмечен, как транспортируемый и у него нет следующей позиции
                # то такой ковш завершил свою последнюю операцию, а значит
                # его нужно переписать в архивную таблицу и удалить из активной
                # удаляю из словаря, чтобы ковш не отображался на сайте
                del ladles_info[str(elem.ladle.id)]
                # переписываю запись из активной таблицы в архивную
                LadlesView.from_active_to_archive(elem)

        return ladles_info

    @staticmethod
    def from_active_to_archive(operation: Type[ActiveDynamicTable]) -> None:
        '''Метод, переписывающий ковш из активной таблицы в архив'''
        # перезаписываю запись в архивную таблицу
        ArchiveDynamicTable.objects.create(
            ladle=operation.ladle,
            num_melt=operation.num_melt,
            brand_steel=operation.brand_steel,
            route=operation.route,
            aggregate=operation.aggregate,
            plan_start=operation.plan_start,
            plan_end=operation.plan_end,
            actual_start=operation.actual_start,
            actual_end=operation.actual_end)
        # удаляю запись из активной таблицы
        operation.delete()
class CranesView(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/cranes.html'
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
    '''Представление страницы с проишествиями'''
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
