from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),     #rota de cadastro
    path('', views.signin, name='signin'),     #rota de login
    path('signout/', views.signout, name='signout'),  #rota de logout
    path('resetPassword/', views.resetPassword, name='resetPassword'),    #rota de reset de senha
    path('resetPassword/<str:token>/', views.resetPassword, name='resetPassword'),    #rota de reset de senha
    path('recoverPassword/', views.recoverPassword, name='recoverPassword'),    #rota de recuperação de senha
    path('logado/', views.logado, name='logado'),    #rota de usuário logado
]