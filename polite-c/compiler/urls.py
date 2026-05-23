"""
URL configuration for compiler app.
"""
from django.urls import path
from . import views

app_name = 'compiler'

urlpatterns = [
    path('', views.ide_home, name='ide_home'),
    path('run/', views.run_code, name='run_code'),
]
