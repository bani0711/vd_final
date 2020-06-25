# config.urls.py
from django.contrib import admin
from django.urls import path
from chart import views                                     # !!!

urlpatterns = [
    path('', views.home, name='home'),
    path('ticket-class/3/',
         views.ticket_class_view_3, name='ticket_class_view_3'),
]
