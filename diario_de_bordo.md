## Ambiente virtual

- Usado como ambiente de trabalho do projeto, onde as dependências do projeto serão instaladas de forma isolada não afetando outros projetos na máquina.

- as dependências do projeto podem ficar registradas no `requirements.txt` pois desta forma sempre que baixar o repositório para uma máquina pode realizar a a instalação das dependências a partir deste arquivo.

- Logo no início criei um `.gitignore` para evitar excessos nos commits e pushs

### Criando, ativando e desativando o ambiente virtual (windows)

```cmd
#cria
python -m venv <nome_ambiente>

#ativa
venv/Scripts/activate

#desativa
venv/Scripts/deactivate

```

### Criando, ativando e desativando o ambiente virtual (linux)

```bash
#cria
python -m venv <nome_ambiente>

#ativa
venv/bin/activate

#desativa
venv/Scripts/deactivate

```

### Registrando dependências usadas no projeto.

```bash
#cria arquivo e salva o nome e versão das dependências usadas no projeto
pip freeze > requirements.txt
```

### Criando Projeto django

```bash
#instalar django no projeto
pip install django

#criar o projeto
django-admin startproject ft_transcendence

#iniciar o projeto (o terminal exibirá qual ip e porta o projeto está rodando)
cd ft_transcendence
python manage.py runserver
  
```

---

## Estrutura do Django
- O django usa Apps para separar os contextos, e cada contexto tem sua lógica de aplicação e negócio e no django cada contexto(ou domínio) é um app, e portanto foi criado uma pasta apps para conter todos os apps, sendo eles até o momento:

- **core**: Lida com a lógica do jogo e funcionalidades principais.
- **custom_auth**: Lida com autenticação de usuários na aplicação
- **users**: Gerencia usuários como cadastro, perfis e sistema de amigos.
- **match**: Representa uma partida e compõe o torneio
- **tournaments**: Para organização de torneios entre jogadores.
- **chat**: Fornece comunicação ao vivo entre amigos.

### Comandos para criar os apps
```bash
    python ../manage.py startapp core
    python ../manage.py startapp custom_auth
    python ../manage.py startapp users
    python ../manage.py startapp match
    python ../manage.py startapp tournaments
    python ../manage.py startapp chat

```

- O Django trabalha com arquitetura MVT (Model, View, Template), parecida com o que a web usa normalmente conhecido como MVC (Model, View, Controller), podemos considerar:
- **MVC**:
	- **Model**: Representa os dados e a lógica de negócio. É responsável por interagir com o banco de dados, validar dados e aplicar regras de negócios.
	- **View**: A parte da interface do usuário, o que o usuário vê e com o que interage (HTML, CSS, etc.).
	- **Controller**: Atua como o intermediário entre o Model e a View. Ele recebe entradas do usuário, chama o Model para manipular os dados e seleciona qual View apresentar ao usuário com base no resultado.
  
- **MVT**:
	- **Model**: Semelhante ao do MVC, o Model no Django também é responsável pela lógica de negócio e interação com o banco de dados.
	- **View**: Diferente do conceito de View no MVC, no Django, a View lida com a lógica de controle (equivalente ao Controller do MVC). Ela processa requisições, interage com o Model e decide qual Template renderizar.
	- **Template**: A camada de apresentação, responsável por gerar o HTML e o que o usuário vê. Isso corresponde à View no MVC.
  
- **Resumo**:
	- **MVC** Model = **MVT** Model
	- **MVC** View = **MVT** Template
	- **MVC** Controller = **MVT** VIew

-  **Outros**:
	- Os conceitos expressos expressos acima podem ser desmembrados em outras camadas como:
		- **Service ou business**: as Models representam apenas as entidades e podem ser mapeadas pelo banco de dados e as regras de negócio ficam nesta nova camada.
		- **Dao ou Repository**: Neste ponto ficam os métodos que constroem as querys e realizam acesso aos dados no banco de dados.
		- ***os diretórios business e repository não foram usados neste projeto.**

- **Estrutura de diretórios:**

```bash
#Estrutura do projeto ft_transcendence
├───apps    # Diretório principal para todos os aplicativos Django do projeto    
│   ├───chat   # Aplicativo para funcionalidades relacionadas a chat   
│   │   ├───__init__.py # Inicializa o pacote Python do aplicativo
│   │   ├───admin.py   # Configurações do admin do Django para o aplicativo
│   │   ├───apps.py    # Config do aplicativo (registro, config adicionais)
│   │   ├───migrations # Migrações de banco de dados 
│   │   │   └───__init__.py # Inicializa o pacote Python das migrações
│   │   ├───models.py # Define os modelos de dados do aplicativo
│   │   ├───static     # Arquivos estáticos   
│   │   ├───templates  # Templates para reúso    
│   │   ├───tests.py   # Testes unitários para o aplicativo
│   │   ├───views.py   # Define as views e lógica das solicitações do aplicativo
│   ├───common_templates          
│   ├───core   # Aplicativo central com funcionalidades do game
│   │   ├───__init__.py 
│   │   ├───admin.py   
│   │   ├───apps.py    
│   │   ├───migrations
│   │   │   └───__init__.py 
│   │   ├───models.py 
│   │   ├───static      
│   │   ├───templates     
│   │   ├───tests.py   
│   │   ├───views.py     
│   ├───custom_auth   # Aplicativo para autenticação personalizada            
│   │   ├───__init__.py 
│   │   ├───admin.py   
│   │   ├───apps.py    
│   │   ├───migrations 
│   │   │   └───__init__.py 
│   │   ├───models.py 
│   │   ├───static     
│   │   ├───templates  
│   │   ├───tests.py 
│   │   ├───views.py          
│   ├───match    # Aplicativo para funcionalidades das partidas      
│   │   ├───__init__.py
│   │   ├───admin.py  
│   │   ├───apps.py   
│   │   ├───migrations
│   │   │   └───__init__.py
│   │   ├───models.py 
│   │   ├───static     
│   │   ├───templates  
│   │   ├───tests.py  
│   │   ├───views.py              
│   ├───static                    
│   │   ├───assets  # Fontes, ícones e outros arquivos de recurso              
│   │   ├───css                   
│   │   │   └───bootstrap         
│   │   │       ├───mixins        
│   │   │       └───utilities     
│   │   └───js                    
│   ├───tournaments   # Aplicativo para funcionalidades relacionadas a torneios    
│   │   ├───__init__.py 
│   │   ├───admin.py   
│   │   ├───apps.py    
│   │   ├───migrations 
│   │   │   └───__init__.py 
│   │   ├───models.py 
│   │   ├───static     
│   │   ├───templates     
│   │   ├───tests.py   
│   │   ├───views.py             
│   └───users        # Aplicativo para funcionalidades relacionadas a usuários   
│   │   ├───__init__.py 
│   │   ├───admin.py  
│   │   ├───apps.py   
│   │   ├───migrations
│   │   │   └───__init__.py 
│   │   ├───models.py 
│   │   ├───static     
│   │   ├───templates    
│   │   ├───tests.py   
│   │   ├───views.py            
└───ft_transcendence # Diretório principal do projeto
│   ├───__init__.py  # Arquivo de inicialização do pacote Django
│   ├───asgi.py      # Configuração do ASGI (Asynchronous Server Gateway Interface)
│   ├───settings.py  # Arquivo de configuração do Django
│   ├───urls.py      # Arquivo de roteamento de URLs do Django
└───└───wsgi.py      # Configuração do WSGI (Web Server Gateway Interface)

```

Os Apps precisam ser registrados para serem reconhecidos:
No arquivo  `settings.py` foram registrados da seguinte forma:

```python

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.custom_auth',           #adicionado
    'apps.chat',                  #adicionado
    'apps.core',                  #adicionado
    'apps.match',                 #adicionado
    'apps.tournaments',           #adicionado
    'apps.users'                  #adicionado
]
```

---
## Setup do Front-End
Para o Front-end usaremos uma abordagem de templates onde teremos uma base que poderá ser reaproveitada e templates de cada app que serão inseridos cada um no seu respectivo momento de acordo com a lógica de negócio implementada.

Para realizar o setup:
- Foram criados diretórios(como pode ser visto anteriormente na árvore)
  - **static** (no diretório apps) este irá conter os arquivos estáticos que podem ser acessados por qualquer app.
  - **common_templates** (no diretório apps) este irá conter os templates base que podem ser reutilizados evitando repetição de código (DRY).
  - **static** e **templates** (no diretório de cada app) estes irão conter cada um em seu app seus templates e arquivos estáticos isolando assim contextos.
- Os diretórios foram registrados no `settings.py` para que o Django possa mapear os arquivos.

```python

"""
Configuração dos paths dos templates da aplicação
"""
TEMPLATES = [

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'apps' / 'common_templates',             # Diretório para templates base
            BASE_DIR / 'apps' / 'chat' / 'templates',           # Templates do chat
            BASE_DIR / 'apps' / 'core' / 'templates',           # Templates do core
            BASE_DIR / 'apps' / 'custom_auth' / 'templates',    # Templates do custom_auth
            BASE_DIR / 'apps' / 'match' / 'templates',          # Templates do match
            BASE_DIR / 'apps' / 'tournaments' / 'templates',    # Templates do tournaments
            BASE_DIR / 'apps' / 'users' / 'templates',          # Templates do users
        ],
        'APP_DIRS': True,      # Permite mapeamento de diretórios dos apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



"""
Configuração dos paths dos diretórios de arquivos estáticos da aplicação
"""
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'

# Diretório para arquivos estáticos comuns (CSS, JS globais, etc.)
STATICFILES_DIRS = [
    BASE_DIR / 'apps' / 'static',                 # Static base para todos os apps
    BASE_DIR / 'apps' / 'chat' / 'static',         # Static do chat
    BASE_DIR / 'apps' / 'core' / 'static',         # Static do core
    BASE_DIR / 'apps' / 'custom_auth' / 'static',  # Static do custom_auth
    BASE_DIR / 'apps' / 'match' / 'static',        # Static do match
    BASE_DIR / 'apps' / 'tournaments' / 'static',  # Static do tournaments
    BASE_DIR / 'apps' / 'users' / 'static',        # Static do users
]
  
# Diretório para arquivos estáticos após o collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'

```

- Uma tela foi configurada para testar o setup e dar início a construção do projeto:
  - **App**: **custom_auth** : responsável pelas regras de autenticação e registro.
  - **tela**: **signin**: tela de login da aplicação que será invocada na rota raiz
    - Para configuração foi necessário:
 		- registrar a rota no arquivo `urls.py` para que  seja possível acessar uma rota pela url e se direcionado para a tela de login usando os templates.
 		- Criação de classe no arquivo `views.py` customizando a interpretação do acesso a rota especificada (como um controller sendo chamado ao acessar uma rota)
 		- definição de Name do aplicativo personalizado no arquivo `apps.py` para que o framework reconheça o aplicativo corretamente disponibilizando-o em toda aplicação de acordo com a configuração realizada em `settings.py` no "INSTALED_APPS".

```python

"""
registrando a rota chamando o controller(view) no urls.py
"""
from django.urls import path

#registrando as views
from apps.custom_auth.views import CustomLoginView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='signin'),     #rota da tela de login (raiz)
]


"""
definindo o nome do template a ser renderizado ao acessar a rota raiz chamando este controller(view) no arquivo views.py
"""
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'signin.html'


"""
definindo o name do app em apps.py para que ele seja reconhecido em toda aplicação assim como foi "instalado" lá em settings.py
"""
from django.apps import AppConfig

class CustomAuthConfig(AppConfig):
    name = 'apps.custom_auth'


```

Feito as configurações acima foi realizado a inserção dos arquivos de Front-End nas pastas devidas e realizado configuração de tags para uso e interpretação de dados pelo django, as tags são:
- **{% load static %}** Carrega o template tag `static` do Django, permitindo o uso de URLs para arquivos estáticos (CSS, JavaScript, imagens) no template.
- **{% block title %}** Define um bloco de conteúdo que pode ser substituído em templates filhos que estendem o template atual.
- **{% block content %}** Define um bloco de conteúdo que pode ser substituído em templates filhos.
- **{% block extra_css %}** Define um bloco de conteúdo para CSS adicional que pode ser incluído em templates filhos.
- **{% block extra_js %}** Define um bloco de conteúdo para JavaScript adicional que pode ser incluído em templates filhos.
- **{% extends 'boilerplate_base.html' %}** Especifica que o template atual herda de um template base.
- **{% csrf_token %}** Insere um token CSRF (Cross-Site Request Forgery) em um formulário para proteger contra ataques CSRF.
- action="**{% url 'signin' %}**"  Usado para especificar de forma explícita a rota a qual o form irá submeter a requisição


Obs.: mais tags serão usadas ao decorrer da criação da aplicação e esta lista será atualizada.
Obs².: para finalizar o setup do front será realizado o uso de arquivos chave valor para idiomas. (em construção)...

---

## Setup do banco de dados

em breve nos cinemas...

