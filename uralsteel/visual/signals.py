from typing import Type

from django.dispatch import Signal
from visual.models import Employees

from .tasks import archive_report_handler

# сигнал отправки отчёта об архивных плавках
archive_report_signal = Signal()


def archive_report_signal_dispatcher(sender, **kwargs) -> None:
    """Функция обработчик сигнала archive_report_signal"""
    user: Type[Employees] = kwargs['user']
    # вызов функции из tasks.py
    archive_report_handler.delay(user.first_name, user.email)


# подключаю обработчик к сигналу
archive_report_signal.connect(archive_report_signal_dispatcher)