from django.urls import path

from . import views

app_name = 'imones'

urlpatterns = [
    path('imones/', views.imoniu_sarasas, name='sarasas'),
    path('imone/<slug:slug>/', views.imone, name='imone'),
    path('imones/duomenys/', views.zemelapio_imones, name='zemelapio_imones'),
]
