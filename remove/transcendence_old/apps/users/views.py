from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.util.utils import is_password_strong, are_fields_empty
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.messages import constants
from django.utils.translation import gettext as getTranslated
from django.contrib.auth import update_session_auth_hash
from minio import Minio
from minio.error import S3Error
from django.conf import settings
from hashlib import sha256
from datetime import datetime

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

        # Configura o cliente MinIO
        minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False  # Defina como True se estiver usando HTTPS
        )

        # Envia a imagem para o MinIO
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            file_extension = profile_picture.name.split('.')[-1]
            # Cria uma hash pequena usando o nome do usuário e a data
            hash_input = f"{user.username}{datetime.now().strftime('%Y%m%d%H%M%S')}"
            small_hash = sha256(hash_input.encode()).hexdigest()[:10]
            file_name = f"profile_pictures/{user.id}/{small_hash}.{file_extension}"
            try:
                minio_client.put_object(
                    settings.MINIO_BUCKET_NAME,
                    file_name,
                    profile_picture,
                    length=profile_picture.size,
                    content_type=profile_picture.content_type
                )
                user.profile_picture = f"{file_name}"  # Salva o caminho da imagem no MinIO
            except S3Error as e:
                messages.error(request, f"Erro ao enviar a imagem: {e}")
        else:
            user.profile_picture = ''

        user.save()  # Salva as alterações no banco de dados
        update_session_auth_hash(request, user)  # Mantém o usuário logado após a troca de senha

        messages.add_message(request, constants.SUCCESS, getTranslated("Perfil atualizado com sucesso"))
        return render(request, 'profile.html', {'user': user})
    if request.htmx:
        return render(request, 'profile.html', {'user': user})
    else:
        return render(request, 'profile_full.html', {'user': user})