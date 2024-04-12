import json

from django.shortcuts import render
from django.views.generic import TemplateView

from visual.mixins import RedisCacheMixin


# Create your views here.

class SimulatorView(TemplateView, RedisCacheMixin):

    template_name = 'simulator/simulator.html'
    # def post(self, request, *args, **kwargs):
    #     """Обработка post-запроса"""
    #     data: dict = json.loads(request.POST.get('cranes_pos'))
    #     # добавление ключа в redis
    #     SimulatorView.set_key_redis_json('cranes_pos', data, 60)
    #     return render(request, self.template_name)