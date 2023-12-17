from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class SimulatorView(TemplateView):

    template_name = 'simulator/simulator.html'