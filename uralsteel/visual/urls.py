from django.urls import path

from visual.views import *

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('ladles/', Ladles.as_view(), name='ladles'),
    path('cranes/', Cranes.as_view(), name='cranes'),
    path('access-denied/', AccessDenied.as_view(), name='access-denied'),
]