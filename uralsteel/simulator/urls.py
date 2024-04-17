from django.urls import path

from simulator.views import *

urlpatterns = [
    path('', SimulatorView.as_view(), name='simulator'),
    ]