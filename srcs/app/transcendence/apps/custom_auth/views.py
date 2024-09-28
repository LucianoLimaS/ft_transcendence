from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.users.models import Users
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import hashlib
from datetime import datetime, timedelta
import re
from django.contrib.auth.hashers import make_password


class CustomLoginView(LoginView):
    template_name = 'signin.html'

# Função de cadastro de usuário
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        description = request.POST.get('description')
        profile_picture = request.POST.get('profile_picture')

        # Verificação de campos vazios
        fields = {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'first_name': first_name,
            'last_name': last_name,
            'description': description,
        }
        
        are_empty, message = are_fields_empty(fields)
        if are_empty:
            return HttpResponse(message)

        if password != confirm_password:
            return HttpResponse("As senhas não conferem")

        # Verificação da força da senha
        is_strong, message = is_password_strong(password)
        if not is_strong:
            return HttpResponse(message)

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verificação de campos vazios
        fields = {
            'username': username,
            'password': password,
        }
        
        are_empty, message = are_fields_empty(fields)
        if are_empty:
            return HttpResponse(message)

        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return redirect('logado')
        else:
            return HttpResponse("Usuário inválido")
    else:
        return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('/')  # Redireciona para a página de login após logout

def recoverPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Verificação de campos vazios
        fields = {
            'username': email,
        }

        user = Users.objects.get(email=email) 

        if user:
            token = makeUniqueHash(user.email + getData())
            user.token = token
            user.token_expires = datetime.now() + timedelta(minutes=15)
            user.save()
            send_mail(
                'Recuperação de senha',
                'o link para recuperação da sua senha é : localhost:8001/resetPassword/' + token,
                settings.DEFAULT_FROM_EMAIL, [user.email], 
                fail_silently=False, 
                )
            return HttpResponse("E-mail Enviado")
        else:
            return HttpResponse("E-mail não cadastrado")
    else:
        return render(request, 'recoverPassword.html')
    
def resetPassword(request, token = None):

    if not token:
        return HttpResponse('Token inválido 1')

    if request.method == 'GET':
        user = Users.objects.filter(token=token);
        if user.exists():
            pass
            return HttpResponse(token)
        else:
            pass
            return HttpResponse('Token inválido 2')
            
    if request.method == 'POST':
        if not token:
            return HttpResponse('Token inválido 3')
        
        try:
            user = Users.objects.get(token=token);
        except Users.DoesNotExist:
            return HttpResponse('Token inválido 4')

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        fields = {
            'username': new_password,
            'password': confirm_password,
        }
        
        are_empty, message = are_fields_empty(fields)
        if are_empty:
            return HttpResponse(message)
        
        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Senhas não conferem', 'token': token})
        
        # Verificação da força da senha
        is_strong, message = is_password_strong(new_password)
        if not is_strong:
            return HttpResponse(message)

        user.password = make_password(new_password)
        user.token = None
        user.token_expires = None
        user.save()
        return redirect('/')
    
    return render(request, 'reset_password.html', {'token': token})

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

def is_password_strong(password):
    # Verifica se a senha tem pelo menos 8 caracteres
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    
    # Verifica se a senha contém pelo menos uma letra maiúscula
    if not re.search(r'[A-Z]', password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    
    # Verifica se a senha contém pelo menos uma letra minúscula
    if not re.search(r'[a-z]', password):
        return False, "A senha deve conter pelo menos uma letra minúscula."
    
    # Verifica se a senha contém pelo menos um dígito
    if not re.search(r'\d', password):
        return False, "A senha deve conter pelo menos um dígito."
    
    # Verifica se a senha contém pelo menos um caractere especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "A senha deve conter pelo menos um caractere especial."
    
    return True, ""

def are_fields_empty(fields):
    for field_name, field_value in fields.items():
        if field_value is None:
            return True, f"O campo {field_name} não pode ser vazio."
        if not field_value.strip():
            return True, f"O campo {field_name} não pode estar vazio."
    return False, ""