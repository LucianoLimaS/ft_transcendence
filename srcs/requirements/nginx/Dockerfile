# Usando a imagem oficial do Nginx como base
FROM nginx:latest

# Remova a configuração padrão do Nginx
# RUN rm /etc/nginx/conf.d/default.conf

# Copie a configuração customizada do Nginx para o container
COPY ./srcs/requirements/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./srcs/requirements/certs /etc/nginx/certs

# Expõe a porta 80 para o tráfego HTTP
EXPOSE 80
EXPOSE 443
