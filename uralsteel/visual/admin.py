from django.contrib import admin

from visual.models import *


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

class AggregatesAdmin(admin.ModelAdmin):
    '''Редактор агрегатов'''
    list_display = '__str__'
    search_fields = 'name'
    fields = (('name', 'num_agg', 'num_pos'),
              ('coord_x', 'coord_y'),
              'stay_time',
              'photo')

class CranesAdmin(admin.ModelAdmin):
    '''Редактор кранов'''
    list_display = '__str__'
    search_fields = 'title'
    fields = ('title',
              ('size_x', 'size_y'),
              'photo')

class LadlesAdmin(admin.ModelAdmin):
    '''Редактор кранов'''
    list_display = '__str__'
    search_fields = 'name'
    fields = ('name', 'is_active')

class BrandSteelAdmin(admin.ModelAdmin):
    '''Редактор марок стали'''
    list_display = '__str__'
    search_fields = 'name'
    fields = 'name'

class DynamicTableAdmin(admin.ModelAdmin):
    '''Редактор динамической таблицы'''
    list_display = '__str__'
    search_fields = ('ladle', 'num_melt', 'brand_steel', 'aggregate')
    fields = (('ladle', 'num_melt', 'brand_steel', 'aggregate'),
              ('plan_start', 'plan_end'),
              ('actual_start', 'actual_end'))

class AccidentsAdmin(admin.ModelAdmin):
    '''Редактор происшетсвий'''
    pass


admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Aggregates, AggregatesAdmin)
admin.site.register(Cranes, CranesAdmin)
admin.site.register(Ladles, LadlesAdmin)
admin.site.register(BrandSteel, BrandSteelAdmin)
admin.site.register(DynamicTable, DynamicTableAdmin)
admin.site.register(ArchiveDynamicTable, DynamicTableAdmin)
admin.site.register(ActiveDynamicTable, DynamicTableAdmin)
admin.site.register(Accidents, AccidentsAdmin)
