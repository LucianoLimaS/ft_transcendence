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
	- **auth**: Lida com autenticação de usuários na aplicação
	- **users**: Gerencia usuários como cadastro, perfis e sistema de amigos.
	- **match**: Representa uma partida e compõe o torneio
	- **tournaments**: Para organização de torneios entre jogadores.
	- **chat**: Fornece comunicação ao vivo entre amigos.
  ### Comandos para criar os apps
```bash
	python ../manage.py startapp core
	python ../manage.py startapp auth
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
    -  **Outros**:
    	- Os conceitos expressos expressos acima podem ser desmembrados em outras camadas como:
     		- **Service ou business**: as Models representam apenas as entidades e podem ser mapeadas pelo banco de dados e as regras de negócio ficam nesta nova camada.
     		- **Dao ou Repository**: Neste ponto ficam os métodos que constroem as querys e realizam acesso aos dados no banco de dados.
     		- *os diretórios business e repository foram criados manualmente*

	- Estrutura de diretórios:
```bash
	my_project/
	├── my_app/
	│   ├── migrations/
	│   ├── static/             # Arquivos estáticos (CSS, JS, etc.)
	│   ├── templates/          # Templates HTML
	│   │   └── my_app/
	│   │       └── template.html  # Exemplo de template
	│   ├── admin.py            # Configuração do Django Admin
	│   ├── apps.py             # Configuração da app Django
	│   ├── models.py           # Definições do Model
	│   ├── views.py            # Funções e classes View
	│   ├── business/           # Camada de regras de negócio 
	│   │ └── entity_business.py # Exemplo de regras de negócio 
	│   ├── repository/         # Camada de repositório para acesso a dados 
	│   │ └── entity_repository.py # Operações de banco de dados
	│   ├── urls.py             # URLs da app
	│   ├── tests.py            # Testes unitários
	│   └── forms.py            # Formulários Django
	├── manage.py
	└── my_project/
	    ├── settings.py         # Configurações do projeto
	    ├── urls.py             # URLs principais do projeto
	    └── wsgi.py             # Configuração do WSGI

```
		

