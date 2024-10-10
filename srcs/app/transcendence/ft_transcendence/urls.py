"""
URL configuration for ft_transcendence project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from apps.chat.views import chat_index  # Importe a função 'index'

urlpatterns = [
    # path('', CustomLoginView.as_view(), name='signin'),  # Tela de login
    path('', include('apps.custom_auth.urls')),  # Rota de autenticação
    path('', include('django_prometheus.urls')),  # Monitoramento
    path('', include('apps.chat.urls')),  # Adicione isso para incluir as URLs do chat
    path('', include('apps.users.urls')),  # Adicione isso para incluir as URLs do usuário
]
