from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),     #rota de cadastro
    path('', views.signin, name='signin'),     #rota de login
    path('signout/', views.signout, name='signout'),  #rota de logout
    path('reset_password/', views.resetPassword, name='reset_password'),    #rota de reset de senha
    path('reset_password/<str:token>/', views.resetPassword, name='reset_password'),    #rota de reset de senha
    path('recover_password/', views.recoverPassword, name='recover_password'),    #rota de recuperação de senha
    path('logado/', views.logado, name='logado'),    #rota de usuário logado
]