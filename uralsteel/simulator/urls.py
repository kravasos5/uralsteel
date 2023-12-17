from django.urls import path

from simulator.views import *

urlpatterns = [
    path('simulator/', SimulatorView.as_view(), name='simulator'),
    ]