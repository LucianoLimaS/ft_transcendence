from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.users.models import Users
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = 'signin.html'

# Função de cadastro de usuário
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        description = request.POST.get('description')
        profile_picture = request.POST.get('profile_picture')

        # Valores padrão para teste
        first_name = "mocado"
        last_name = "mocado"
        description = "mocado"
        profile_picture = "mocado"

        user = Users.objects.filter(username=username);
        if user:
            return HttpResponse("Usuário já cadastrado")
        else:
            user = Users.objects.create_user(
                username = username,
                email= email,
                password= password,
                first_name= first_name,
                last_name= last_name,
                description= description,
                profile_picture= profile_picture,
                )
            user.save()
            return redirect('/')
    else:
        return render(request, 'signup.html')

# Função de login
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return redirect('logado')
        else:
            return HttpResponse("Usuário inválido1")
    
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/')  # Redireciona para a página de login após logout



@login_required(login_url='/')
def logado(request):
    return HttpResponse('você está logado')