import os, time

import pandas
from celery import shared_task
from django.core.mail import EmailMessage
from uralsteel.settings import MEDIA_ROOT
from .models import ArchiveDynamicTable

@shared_task()
def archive_report_handler(user_first_name, user_email):
    '''Функция отправки архивного отчёта на почту по запросу пользователя'''
    mail = EmailMessage(
        "Письмо с отчётом",
        f"Здравствуйте, {user_first_name}, вы запросили отчёт, вот он:",
        "uralsteel@gmail.com",
        [f"{user_email}"],
    )
    # извлекаю дату из БД
    data = ArchiveDynamicTable.objects.all().values('id')
    # с помощью pandas конвертирую в xlsx
    df = pandas.DataFrame.from_records(data)
    path_to_file: str = os.path.join(MEDIA_ROOT, 'archive_reports/report.xlsx')
    df.to_excel(path_to_file, sheet_name='Archive-Report', index=False)
    # прикрепляю xlsx-документ
    with open(path_to_file, 'rb') as excel_file:
        mail.attach(path_to_file, excel_file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # эмулирую долгую операцию
    time.sleep(10)
    # отправляю письмо
    mail.send()
