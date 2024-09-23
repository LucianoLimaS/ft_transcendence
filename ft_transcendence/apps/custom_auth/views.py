from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.users.models import Users
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import hashlib
from datetime import datetime

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

def recoverPassword(request):
    if request.method == 'GET':
        email = request.POST.get('email')
        user = Users.objects.get(email=email) 
        if user:
            token = makeUniqueHash(user.email + getData())
            user.token = token
            user.token_expires = datetime.now()
            user.save()
            send_mail(
                'Recuperação de senha',
                'o link para recuperação da sua senha é : localhost:8080/changePassword/' + token,
                settings.DEFAULT_FROM_EMAIL, [user.email], 
                fail_silently=False, 
                )
            return HttpResponse("E-mail Enviado")
        else:
            return HttpResponse("E-mail não cadastrado")
    else:
        return render(request, 'recoverPassword.html')
    
def reset_password(request, token, email, password):
    pass

@login_required(login_url='/')
def logado(request):
    return HttpResponse('você está logado')

def makeUniqueHash(input_string):
    # Cria um objeto de hash SHA-256
    sha256 = hashlib.sha256()
    
    # Atualiza o objeto de hash com a string de entrada codificada
    sha256.update(input_string.encode('utf-8'))
    
    # Retorna o hash hexadecimal gerado
    return sha256.hexdigest()

def getData():
    # Obter a data e hora atuais
    agora = datetime.now()
    
    # Formatar a data e hora no formato desejado
    data_hora_formatada = agora.strftime('%d/%m/%Y %H:%M:%S')
    
    return data_hora_formatada