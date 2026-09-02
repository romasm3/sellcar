from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('', views.conversation_list, name='list'),
    path('<int:pk>/', views.conversation_detail, name='detail'),
    path('<int:pk>/translate/', views.translate_conversation, name='translate'),
    path('<int:pk>/translate/toggle/', views.translate_toggle, name='translate_toggle'),
    path('start/<int:listing_id>/', views.start_conversation, name='start'),
    path('check-new/', views.check_new_messages, name='check_new'),
    path('support/', views.start_support_conversation, name='start_support'),
]