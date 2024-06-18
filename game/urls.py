from django.urls import path, include
from . import views

app_name = 'game'

urlpatterns = [
    path('index', views.index, name = 'index'),
    path('mariokart', views.mario, name = 'mariokart'),
    path('lol', views.lol, name = 'lol'),
    path('splatoon', views.splatoon, name = 'splatoon'),
]