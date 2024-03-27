import time

from celery import Celery


celery = Celery('tasks', broker='redis://127.0.0.1:6379', broker_connection_retry_on_startup=True)


@celery.task
def archive_report_handler(user_first_name: str, user_email: str):
    """Функция отправки архивного отчёта на почту по запросу пользователя"""
    mail = f'Письмо с отчётом. Здравствуйте, {user_first_name}, вы запросили отчёт, вот он: uralsteel@gmail.com {user_email}'
    # извлекаю дату из БД
    # с помощью pandas конвертирую в xlsx
    # прикрепляю xlsx-документ
    # моделирую долгую операцию
    time.sleep(10)
    # отправляю письмо
    # тут бдет логика отправки письма
    print(mail)
