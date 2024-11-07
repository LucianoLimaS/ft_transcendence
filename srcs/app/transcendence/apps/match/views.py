from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def pong(request):
    if request.htmx:
        return render(request, 'pong.html')
    else:
        return render(request, 'pong.html')