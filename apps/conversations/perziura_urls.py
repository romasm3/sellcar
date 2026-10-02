"""/administracija/… — pokalbių peržiūra ginčams (apps/conversations/perziura.py)."""
from django.urls import path

from . import perziura

app_name = 'pokalbiu_perziura'

urlpatterns = [
    path('pokalbiai/', perziura.sarasas, name='sarasas'),
    path('pokalbiai/<int:pk>/', perziura.gija, name='gija'),
    path('zurnalas/', perziura.zurnalas, name='zurnalas'),
]
