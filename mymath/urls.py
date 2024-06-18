from django.urls import path
from . import views

app_name = "mymath"

urlpatterns = [
  path('height_quiz/', views.height_quiz_view, name='height_quiz'),
]
