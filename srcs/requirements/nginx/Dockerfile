# Usando a imagem oficial do Nginx como base
FROM nginx:latest

# Remova a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copie a configuração customizada do Nginx para o container
COPY ./requirements/nginx/nginx.conf /etc/nginx/nginx.conf

# Copie o diretório de arquivos estáticos do host para o container (opcional)
# Se estiver usando volumes no Docker Compose, pode omitir essa parte
# COPY ./static /static

# Expõe a porta 80 para o tráfego HTTP
EXPOSE 80
