from django.urls import path

from visual.views import *

urlpatterns = [
    path('main/', Main.as_view(), name='main'),
]