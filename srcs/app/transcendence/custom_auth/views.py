from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.messages import constants
from django.contrib import messages
from django.utils.translation import gettext as getTranslated
from django.http import JsonResponse
from django.urls import reverse
from util.utils import makeUniqueHash, getData, is_password_strong, are_fields_empty  # Importe a função global
from django.utils import timezone
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.utils import timezone

class CustomLoginView(LoginView):
    template_name = 'signin.html'

# Função de cadastro de usuário
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Verificação de campos vazios
        fields = {
            'username': username,
            'e-mail': email,
            'password': password,
            'confirm password': confirm_password,
        }
        are_empty, message = are_fields_empty(fields)
        if are_empty:
            messages.add_message(request, constants.ERROR, getTranslated(message))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})

        if password != confirm_password:
            messages.add_message(request, constants.ERROR, getTranslated("As senhas não conferem"))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        
        # Verificação da força da senha
        is_strong, message = is_password_strong(password)
        if not is_strong:
            messages.add_message(request, constants.ERROR, getTranslated(message))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        
        user = User.objects.filter(email=email);
        if user:
            messages.add_message(request, constants.ERROR, getTranslated("Email already registered"))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        
        user = User.objects.filter(username=username);
        if user:
            messages.add_message(request, constants.ERROR, getTranslated("User already registered"))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
            first_name = "",
            last_name = "",
            )
        user.save()
        messages.add_message(request, constants.SUCCESS, getTranslated("User registered successfully"))
        # Passa o objeto messages para o template
        return JsonResponse({
                "redirect": reverse('signin')  # Usando a URL da view 'logado'
        })
    else:
        if request.htmx:
            return render(request, 'signup.html')
        else:
            return render(request, 'signup_full.html')


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
            messages.add_message(request, constants.ERROR, getTranslated(message))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            user.last_login = timezone.now()
            user.save()
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    "redirect": reverse('home')  # Usando a URL da view 'logado'
                })
            else:
                # Full request (non-HTMX), redirect to main page
                return JsonResponse({
                    "redirect": reverse('home')  # Usando a URL da view 'logado'
                })
        else:
            messages.add_message(request, constants.ERROR, getTranslated("Invalid username or password!"))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
    else:
        if request.htmx:
            return render(request, 'signin.html')
        else:
            return render(request, 'signin_full.html')


def signout(request):
    logout(request)
    return redirect('/')  # Redireciona para a página de login após logout

def recoverPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Verificação de campos vazios
        fields = {
            'e-mail': email,
        }
        are_empty, message = are_fields_empty(fields)
        if are_empty:
            messages.add_message(request, constants.ERROR, getTranslated(message))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.add_message(request, constants.ERROR, getTranslated("E-mail not registered."))
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        
        if user:
            token = makeUniqueHash(user.email + getData())
            user.token = token
            user.token_expires = timezone.now() + timedelta(minutes=15)
            user.save()
            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=user.email,
                subject='Recuperação de senha',
                html_content='o link para recuperação da sua senha é : localhost:8001/reset_password/' + token)
            try:
                sg = SendGridAPIClient(settings.EMAIL_API_KEY)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
            messages.add_message(request, constants.SUCCESS, getTranslated("E-mail sent successfully."))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        else:
            messages.add_message(request, constants.ERROR, getTranslated("E-mail not registered."))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
    else:
        if request.htmx:
            return render(request, 'recoverPassword.html')
        else:
            return render(request, 'recoverPassword_full.html')
    
def resetPassword(request, token = None):
    if not token:
        messages.add_message(request, constants.ERROR, getTranslated("Invalid token."))
        return render(request, 'recoverPassword_full.html', {"messages": messages.get_messages(request)})

    if request.method == 'GET':
        user = User.objects.filter(token=token);
        if user.exists():
            return render(request, 'resetPassword_full.html', {'token': token})
        else:
            messages.add_message(request, constants.ERROR, getTranslated("Invalid token."))
            return render(request, 'recoverPassword_full.html', {"messages": messages.get_messages(request)})
            
    if request.method == 'POST':
        if not token:
            messages.add_message(request, constants.ERROR, getTranslated("Invalid token."))
            return render(request, 'recoverPassword_full.html', {"messages": messages.get_messages(request)})
        
        try:
            user = User.objects.get(token=token);
        except User.DoesNotExist:
            messages.add_message(request, constants.ERROR, getTranslated("Invalid token."))
            return render(request, 'recoverPassword_full.html', {"messages": messages.get_messages(request)})

        if user.token_expires < timezone.now():
            messages.add_message(request, constants.ERROR, getTranslated("Token expired."))
            return render(request, 'recoverPassword_full.html', {"messages": messages.get_messages(request)})
        
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        fields = {
            'password': password,
            'confirm password': confirm_password,
        }
        
        are_empty, message = are_fields_empty(fields)
        if are_empty:
            messages.add_message(request, constants.ERROR, getTranslated(message))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        
        if password != confirm_password:
            messages.add_message(request, constants.ERROR, getTranslated("As senhas não conferem"))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})
        
        # Verificação da força da senha
        is_strong, message = is_password_strong(password)
        if not is_strong:
            messages.add_message(request, constants.ERROR, getTranslated(message))
            # Passa o objeto messages para o template
            return render(request, "response.html", {"messages": messages.get_messages(request)})

        user.password = make_password(password)
        user.token = None
        user.token_expires = None
        user.save()
        response = JsonResponse({'location': '/'})
        response['HX-Redirect'] = '/'
        return response
    return render(request, 'resetPassword_full.html')