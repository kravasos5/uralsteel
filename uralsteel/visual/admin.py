from django.contrib import admin

from visual.models import *
from django.contrib import admin


class EmployeesAdmin(admin.ModelAdmin):
    """Редактор ползователя"""
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
    """Редактор агрегатов"""
    list_display = ('__str__',)
    search_fields = ('title',)
    fields = (('title', 'num_agg', 'num_pos'),
              ('coord_x', 'coord_y'), 'is_broken',
              'stay_time',
              'photo')

class RoutesAdmin(admin.ModelAdmin):
    """Редактор маршрутов"""
    list_display = ('__str__',)
    fields = ('aggregate_1', 'aggregate_2', 'aggregate_3', 'aggregate_4')

class CranesAdmin(admin.ModelAdmin):
    """Редактор кранов"""
    list_display = ('__str__',)
    search_fields = ('title',)
    fields = ('title',
              ('size_x', 'size_y'),
              'photo', 'is_broken')

class LadlesAdmin(admin.ModelAdmin):
    """Редактор кранов"""
    list_display = ('__str__',)
    search_fields = ('title',)
    fields = ('title', 'is_active', 'is_broken')

class BrandSteelAdmin(admin.ModelAdmin):
    """Редактор марок стали"""
    list_display = ('__str__',)
    search_fields = ('title',)
    fields = ('title',)

class DynamicTableAdmin(admin.ModelAdmin):
    """Редактор динамической таблицы"""
    list_display = ('__str__',)
    search_fields = ('ladle', 'num_melt', 'brand_steel', 'route', 'aggregate')
    fields = (('ladle', 'num_melt', 'brand_steel', 'route', 'aggregate'),
              ('plan_start', 'plan_end'),
              ('actual_start', 'actual_end'))

class AccidentAdmin(admin.ModelAdmin):
    """Редактор происшетсвий"""
    list_display = ('__str__',)
    search_fields = ('author', 'object', 'created_at')
    fields = ('object', 'author', 'report', 'created_at')
    readonly_fields = ('author', 'created_at')

admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Aggregates, AggregatesAdmin)
admin.site.register(AggregatesGMP, AggregatesAdmin)
admin.site.register(AggregatesUKP, AggregatesAdmin)
admin.site.register(AggregatesUVS, AggregatesAdmin)
admin.site.register(AggregatesMNLZ, AggregatesAdmin)
admin.site.register(AggregatesL, AggregatesAdmin)
admin.site.register(AggregatesBurner, AggregatesAdmin)
admin.site.register(Routes, RoutesAdmin)
admin.site.register(Cranes, CranesAdmin)
admin.site.register(Ladles, LadlesAdmin)
admin.site.register(BrandSteel, BrandSteelAdmin)
admin.site.register(ArchiveDynamicTable, DynamicTableAdmin)
admin.site.register(ActiveDynamicTable, DynamicTableAdmin)
admin.site.register(LadlesAccident, AccidentAdmin)
admin.site.register(CranesAccident, AccidentAdmin)
admin.site.register(AggregatAccident, AccidentAdmin)