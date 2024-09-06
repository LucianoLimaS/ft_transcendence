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

