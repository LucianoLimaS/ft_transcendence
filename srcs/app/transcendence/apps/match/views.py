from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def pong(request):
    if request.htmx:
        return render(request, 'pong.html')
    else:
        return render(request, 'pong.html')
    
def pongLocal(request):
    if request.htmx:
        return render(request, 'pong_local.html')
    else:
        return render(request, 'pong_local_full.html')