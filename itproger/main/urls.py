from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contacs', views.contacs, name='contacs'),
    path('weather/', views.weather, name='weather'),
    path('currency/', views.currency, name='currency'),
]




