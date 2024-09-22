from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),     #rota de cadastro
    path('', views.signin, name='signin'),     #rota de login
    path('signout/', views.signout, name='signout'),  #rota de logout
    path('reset_password/', views.reset_password, name='reset_password'),    #rota de reset de senha
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),    #rota de reset de senha
    path('reset_password/<str:token>/<str:email>/', views.reset_password, name='reset_password'),    #rota de reset de senha
    path('reset_password/<str:token>/<str:email>/<str:password>/', views.reset_password, name='reset_password'),    #rota de reset de senha
    path('logado/', views.logado, name='logado'),    #rota de usuário logado
]