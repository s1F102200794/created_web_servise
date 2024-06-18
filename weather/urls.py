from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('index/', views.Japan_weather, name = 'index'),
    path('Hokkaido/', views.Hokkaido_weather, name = 'Hokkaido'),
    path('Tohoku/', views.Tohoku_weather, name = 'Tohoku'),
    path('Kanto/', views.Kanto_weather, name = 'Kanto'),
    path('Chubu/', views.Chubu_weather, name = 'Chubu'),
    path('Kinki/', views.Kinki_weather, name = 'Kinki'),
    path('Chugoku/', views.Chugoku_weather, name = 'Chugoku'),
    path('Shikoku/', views.Shikoku_weather, name = 'Shikoku'),
    path('Kyusyu/', views.Kyusyu_weather, name = 'Kyusyu'),
]