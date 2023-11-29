from django.contrib import admin

from visual.models import Employees


class EmployeesAdmin(admin.ModelAdmin):
    '''Редактор ползователя'''
    list_display = ('__str__', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'patronymic')
    fields = (('username', 'email'), ('first_name', 'last_name', 'patronymic'),
              ('photo'),
              'post',
              ('send_messages'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    exclude = ('slug',)
    readonly_fields = ('last_login', 'date_joined')

admin.site.register(Employees, EmployeesAdmin)