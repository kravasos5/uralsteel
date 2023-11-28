from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Employees(AbstractUser):
    '''Модель работника'''

    POSTS_CHOICES = (
        ('MS', 'Master'),
        ('MH', 'Mechanic'),
        ('DT', 'Dispatcher'),
    )

    def get_photo_path(instance, filename):
        # получения пути сохранения фото
        username = instance.username
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
    post = models.CharField(max_length=2, choices=POSTS_CHOICES)
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name='Отчество')
    slug = models.SlugField(max_length=200, unique=True, db_index=True,
                            verbose_name='Слаг')

    class Meta(AbstractUser.Meta):
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return f'<{self.username}>'

    def get_absolute_url(self):
        return reverse('visual:employee-profile', kwargs={'slug': self.slug})




class Aggregates(models.Model):
    '''Модель агрегатов (справочная информация)'''

    def get_photo_path(instance, filename):
        # получения пути сохранения фото
        return f'photos/aggregates/{filename}'

    name = models.CharField(verbose_name="Название агрегата", max_length=100)
    num_agg = models.CharField(verbose_name="Номер агрегата", max_length=100)
    num_pos = models.CharField(verbose_name="Номер позиции", max_length=100)
    coord_x = models.SmallIntegerField(verbose_name="Координата по Х")
    coord_y = models.SmallIntegerField(verbose_name="Координата по У")
    stay_time = models.DateTimeField(verbose_name="Время пребывания на агрегате")
    photo = models.ImageField(upload_to=get_photo_path, verbose_name="Фото ковша на агрегате")

    def __str__(self):
        return f'{self.name} {self.num_agg} {self.num_pos}'

    class Meta:
        verbose_name = 'Агрегат'
        verbose_name_plural = 'Агрегаты'

class Cranes(models.Model):
    '''Модель кранов'''

    def get_photo_path(instance, filename):
        # получения пути сохранения фото
        return f'photos/cranes/{filename}'

    title = models.CharField(verbose_name="Название крана или каретки", max_length=100)
    size_x = models.SmallIntegerField(verbose_name="Размер по Х")
    size_y = models.SmallIntegerField(verbose_name="Размер по У")
    photo = models.ImageField(upload_to="", verbose_name="Фото крана или каретки")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Кран'
        verbose_name_plural = 'Краны'

class Ladles(models.Model):
    '''Модель ковшей'''

    name = models.CharField(verbose_name="Название ковша", max_length=100)
    is_active = models.BooleanField(default=False, verbose_name="Активен ли ковш")
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ковш'
        verbose_name_plural = 'Ковши'

class BrandSteel(models.Model):
    '''Модель марок стали'''

    name = models.CharField(verbose_name="Марка стали", max_length=100)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Марка стали'
        verbose_name_plural = 'Марки стали'

class DynamicTable(models.Model):
    '''Основная таблица с информацией о перемещении ковшей в реальном времени'''

    ladle = models.ForeignKey('Ladles', on_delete=models.PROTECT, verbose_name='Ковш')
    num_melt = models.CharField(max_length=100, unique=True, verbose_name='Номер плавки')
    brand_steel = models.CharField(max_length=100, verbose_name='Марка стали')
    aggregate = models.ForeignKey('Aggregates', on_delete=models.PROTECT, verbose_name='Агрегат')
    plan_start = models.DateTimeField(verbose_name='Плановая дата начала')
    plan_end = models.DateTimeField(verbose_name='Плановая дата завершения')
    actual_start = models.DateTimeField(verbose_name='Фактическая дата начала')
    actual_end = models.DateTimeField(verbose_name='Фактическая дата завершения')

    def __str__(self):
        return f'{self.num_melt}'

    class Meta:
        verbose_name = 'Плавка'
        verbose_name_plural = 'Плавки'

class Accidents(models.Model):
    '''Модель происшествий'''
    pass