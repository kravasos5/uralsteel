from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify


class Employees(AbstractUser):
    """Модель работника"""

    POSTS_CHOICES = (
        ('MS', 'Master'),
        ('MH', 'Mechanic'),
        ('DT', 'Dispatcher'),
    )

    def get_photo_path(self, filename):
        # получения пути сохранения фото
        username = self.username
        return f'photos/{username}/{filename}'

    def save(self, *args, **kwargs):
        # нужно добавить slug в правильном формате перед сохранением
        if not self.slug:
            self.slug = slugify(f'{self.username}')
        super().save(*args, **kwargs)

    send_messages = models.BooleanField(default=True,
                                        verbose_name='Слать оповещения на почту?')
    photo = models.ImageField(verbose_name='Фото работника',
                              upload_to=get_photo_path,
                              null=True)
    post = models.CharField(max_length=2, choices=POSTS_CHOICES, verbose_name='Должность')
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name='Отчество')
    slug = models.SlugField(max_length=200, unique=True, db_index=True,
                            verbose_name='Слаг')

    class Meta(AbstractUser.Meta):
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return f'<{self.username}>'

    def get_absolute_url(self):
        # Формирование ссылки на профиль пользователя
        return reverse('profile', kwargs={'slug': self.slug})


class Aggregates(models.Model):
    """Модель агрегатов (справочная информация)"""

    def get_photo_path(self, filename):
        # получения пути сохранения фото
        return f'photos/aggregates/{filename}'

    title = models.CharField(verbose_name="Название агрегата", max_length=100)
    num_agg = models.CharField(verbose_name="Номер агрегата", max_length=100)
    num_pos = models.CharField(verbose_name="Номер позиции", max_length=100)
    coord_x = models.SmallIntegerField(verbose_name="Координата по Х")
    coord_y = models.SmallIntegerField(verbose_name="Координата по У")
    stay_time = models.TimeField(verbose_name="Время пребывания на агрегате")
    photo = models.ImageField(upload_to=get_photo_path, verbose_name="Фото ковша на агрегате")
    is_broken = models.BooleanField(default=False, null=False, blank=False,
                                    verbose_name="Сломан ли агрегат")

    def __str__(self):
        return f'{self.title}-{self.num_agg}-{self.num_pos}'

    class Meta:
        verbose_name = 'Агрегат'
        verbose_name_plural = 'Агрегаты'


class AggregatesGMP(Aggregates):
    """Модель агрегатов ГМП"""

    class Meta:
        verbose_name = 'Агрегат ГМП'
        verbose_name_plural = 'Агрегаты ГМП'


class AggregatesUKP(Aggregates):
    """Модель агрегатов УКП"""

    class Meta:
        verbose_name = 'Агрегат УКП'
        verbose_name_plural = 'Агрегаты УКП'


class AggregatesUVS(Aggregates):
    """Модель агрегатов УВС"""

    class Meta:
        verbose_name = 'Агрегат УВС'
        verbose_name_plural = 'Агрегаты УВС'


class AggregatesMNLZ(Aggregates):
    """Модель агрегатов МНЛЗ"""

    class Meta:
        verbose_name = 'Агрегат МНЛЗ'
        verbose_name_plural = 'Агрегаты МНЛЗ'


class AggregatesL(Aggregates):
    """Модель агрегатов Лёжек"""

    class Meta:
        verbose_name = 'Лежка'
        verbose_name_plural = 'Лежки'


class AggregatesBurner(Aggregates):
    """Модель агрегатов Горелок"""

    class Meta:
        verbose_name = 'Горелка'
        verbose_name_plural = 'Горелки'


class Routes(models.Model):
    """Модель маршрутов"""

    aggregate_1 = models.ForeignKey('AggregatesGMP', on_delete=models.PROTECT, verbose_name='Номер ГМП')
    aggregate_2 = models.ForeignKey('AggregatesUKP', on_delete=models.PROTECT, verbose_name='Номер УКП')
    aggregate_3 = models.ForeignKey('AggregatesUVS', on_delete=models.PROTECT, verbose_name='Номер УВС')
    aggregate_4 = models.ForeignKey('AggregatesMNLZ', on_delete=models.PROTECT, verbose_name='Номер МНЛЗ')

    def __str__(self):
        return f'{self.aggregate_1}, {self.aggregate_2}, {self.aggregate_3}, {self.aggregate_4}'

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'


class Cranes(models.Model):
    """Модель кранов"""

    def get_photo_path(self, filename):
        # получения пути сохранения фото
        return f'photos/cranes/{filename}'

    title = models.CharField(verbose_name="Название крана или каретки", max_length=100)
    size_x = models.SmallIntegerField(verbose_name="Размер по Х")
    size_y = models.SmallIntegerField(verbose_name="Размер по У")
    photo = models.ImageField(upload_to=get_photo_path, verbose_name="Фото крана или каретки")
    is_broken = models.BooleanField(default=False, null=False, blank=False,
                                    verbose_name="Сломан ли кран")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Кран'
        verbose_name_plural = 'Краны'


class Ladles(models.Model):
    """Модель ковшей"""

    title = models.CharField(verbose_name="Название ковша", max_length=100)
    is_active = models.BooleanField(default=False, null=False, blank=False,
                                    verbose_name="Активен ли ковш")
    is_broken = models.BooleanField(default=False, null=False, blank=False,
                                    verbose_name="Сломан ли ковш")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Ковш'
        verbose_name_plural = 'Ковши'


class BrandSteel(models.Model):
    """Модель марок стали"""

    title = models.CharField(verbose_name="Марка стали", max_length=100)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Марка стали'
        verbose_name_plural = 'Марки стали'


class DynamicTableAbstract(models.Model):
    """Основная таблица с информацией о перемещении ковшей в реальном времени"""

    ladle = models.ForeignKey('Ladles', on_delete=models.PROTECT, verbose_name='Ковш')
    num_melt = models.CharField(max_length=100, verbose_name='Номер плавки')
    brand_steel = models.ForeignKey('BrandSteel', on_delete=models.PROTECT, max_length=100, verbose_name='Марка стали')
    route = models.ForeignKey('Routes', on_delete=models.PROTECT, verbose_name='Маршрурт')
    aggregate = models.ForeignKey('Aggregates', on_delete=models.PROTECT, verbose_name='Агрегат')
    plan_start = models.DateTimeField(verbose_name='Плановая дата начала')
    plan_end = models.DateTimeField(verbose_name='Плановая дата завершения')
    actual_start = models.DateTimeField(null=True, verbose_name='Фактическая дата начала')
    actual_end = models.DateTimeField(null=True, verbose_name='Фактическая дата завершения')

    def __str__(self):
        return f'{self.num_melt}'

    class Meta:
        abstract = True


class ArchiveDynamicTable(DynamicTableAbstract):
    """Модель архивных записей динамической таблицы"""

    def __str__(self):
        return f'Архивная плавка №{self.num_melt}'

    class Meta:
        verbose_name = 'Архивная плавка'
        verbose_name_plural = 'Архивные плавки'
        ordering = ('-actual_end',)


class ActiveDynamicTable(DynamicTableAbstract):
    """Модель активных записей динамической таблицы"""

    def __str__(self):
        return f'Активная плавка №{self.num_melt}'

    class Meta:
        verbose_name = 'Активная плавка'
        verbose_name_plural = 'Активные плавки'
        ordering = ('-actual_end',)


@deconstructible
class WordCountValidator(object):
    """Валидатор количества слова"""

    def __init__(self, count):
        self.count = count

    def __call__(self, val):
        # Проверка оличества слов
        if len(str(val).split(' ')) < self.count:
            raise ValidationError('Отчёт должен содержать как ' +
                                  'минимум %(count)s слов',
                                  code='not_enough_words',
                                  params={'count': self.count})

    def __eq__(self, other):
        return self.count == other.count


class AccidentsAbstract(models.Model):
    """Модель происшествий"""

    author = models.ForeignKey(Employees, on_delete=models.SET_NULL,
                               null=True, blank=False,
                               verbose_name='Автор отчёта')
    report = models.CharField(max_length=800, validators=[WordCountValidator(10)],
                              null=True, blank=False, default=None,
                              verbose_name='Подробное описание проблемы')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания отчёта')

    class Meta:
        abstract = True


def accident_pre_save_dispatcher(sender, **kwargs):
    """Диспетчер выполняющийся перед созданием нового проишествия"""
    instance = kwargs['instance']
    object = instance.object
    # отмечаю кран/ковш/агрегат как сломанный
    object.is_broken = True
    object.save()
    # дальнейшая обработка перестроения маршрутов
    ...


class LadlesAccident(AccidentsAbstract):
    """Модель проишествий ковшей"""
    object = models.ForeignKey(Ladles, on_delete=models.SET_NULL,
                               null=True, blank=False,
                               verbose_name='Ковш')

    def __str__(self):
        return f'Отчёт ковш №{self.object.id} - {self.created_at}'

    class Meta:
        verbose_name = 'Прошествия с ковшом'
        verbose_name_plural = 'Прошествия с ковшами'
        ordering = ('-created_at',)


pre_save.connect(accident_pre_save_dispatcher, sender=LadlesAccident)


class CranesAccident(AccidentsAbstract):
    """Модель проишествий кранов"""
    object = models.ForeignKey(Cranes, on_delete=models.SET_NULL,
                               null=True, blank=False,
                               verbose_name='Кран')

    def __str__(self):
        return f'Отчёт кран №{self.object.id} - {self.created_at}'

    class Meta:
        verbose_name = 'Прошествия с краном'
        verbose_name_plural = 'Прошествия с кранами'
        ordering = ('-created_at',)


pre_save.connect(accident_pre_save_dispatcher, sender=CranesAccident)


class AggregatAccident(AccidentsAbstract):
    """Модель проишествий агрегатов"""
    object = models.ForeignKey(Aggregates, on_delete=models.SET_NULL,
                               null=True, blank=False,
                               verbose_name='Агрегат')

    def __str__(self):
        return f'Отчёт агрегат №{self.object.id} - {self.created_at}'

    class Meta:
        verbose_name = 'Прошествия с агрегатом'
        verbose_name_plural = 'Прошествия с агрегатами'
        ordering = ('-created_at',)


pre_save.connect(accident_pre_save_dispatcher, sender=AggregatAccident)
