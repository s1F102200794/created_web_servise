from django.urls import path
from . import views

app_name = 'chatGPT'

urlpatterns = [
    path('index/', views.Japan_weather_gpt, name = 'index'),
    path('Hokkaido/', views.Hokkaido_weather_gpt, name = 'Hokkaido'),
    path('Tohoku/', views.Tohoku_weather_gpt, name = 'Tohoku'),
    path('Kanto/', views.Kanto_weather_gpt, name = 'Kanto'),
    path('Chubu/', views.Chubu_weather_gpt, name = 'Chubu'),
    path('Kinki/', views.Kinki_weather_gpt, name = 'Kinki'),
    path('Chugoku/', views.Chugoku_weather_gpt, name = 'Chugoku'),
    path('Shikoku/', views.Shikoku_weather_gpt, name = 'Shikoku'),
    path('Kyusyu/', views.Kyusyu_weather_gpt, name = 'Kyusyu'),
]