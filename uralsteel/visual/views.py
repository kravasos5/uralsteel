from django.shortcuts import render
from django.views.generic import TemplateView


class Main(TemplateView):
    '''Представление главной страницы'''
    template_name = 'visual/main.html'

class Ladles(TemplateView):
    '''Представление страницы с ковшами'''
    template_name = 'visual/ladles.html'

class Cranes(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/cranes.html'

class AccessDenied(TemplateView):
    '''Представление страницы с кранами'''
    template_name = 'visual/access_denied.html'
