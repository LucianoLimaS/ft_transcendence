from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.util.utils import is_password_strong, are_fields_empty
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.messages import constants
from django.utils.translation import gettext as getTranslated
from django.contrib.auth import update_session_auth_hash
# Create your views here.

@login_required(login_url='/')
def profile(request):
    user = request.user  # Obtém o usuário logado
    if request.method == 'POST':
        # Atualiza os campos manualmente
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = ""
        user.description = request.POST.get('description')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        fields = {
            'password': password,
            'confirm password': confirm_password,
        }
        
        are_empty, message = are_fields_empty(fields)
        if not are_empty:
        
            if password != confirm_password:
                messages.add_message(request, constants.ERROR, getTranslated("As senhas não conferem"))
                # Passa o objeto messages para o template
                return render(request, "profile.html", {'user': user, "messages": messages.get_messages(request)})
            
            # Verificação da força da senha
            is_strong, message = is_password_strong(password)
            if not is_strong:
                messages.add_message(request, constants.ERROR, getTranslated(message))
                # Passa o objeto messages para o template
                return render(request, "profile.html", {'user': user, "messages": messages.get_messages(request)})
            user.set_password(password)

        # Se houver upload de imagem
        """ if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture'] """
        user.profile_picture = ''

        user.save()  # Salva as alterações no banco de dados
        update_session_auth_hash(request, user)  # Mantém o usuário logado após a troca de senha

        messages.add_message(request, constants.SUCCESS, getTranslated("Perfil atualizado com sucesso"))
        return render(request, 'profile.html', {'user': user})
    if request.htmx:
        return render(request, 'profile.html', {'user': user})
    else:
        return render(request, 'profile_full.html', {'user': user})