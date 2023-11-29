from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.deconstruct import deconstructible
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