from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
  return render(request, 'game/index.html')

@login_required
def mario(request):
  return render(request, 'game/mariokart.html')

@login_required
def lol(request):
  return render(request, 'game/lol.html')

@login_required
def splatoon(request):
  return render(request, 'game/splatoon.html')