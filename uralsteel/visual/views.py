from django.shortcuts import render
from django.views.generic import TemplateView


class Main(TemplateView):
    '''Представление главной страницы'''
    template_name = 'visual/main.html'
