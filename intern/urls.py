from django.urls import path, include
from . import views

app_name = 'intern'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('home/', views.home, name='home'),
]