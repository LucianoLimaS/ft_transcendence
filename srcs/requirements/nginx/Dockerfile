# Usando a imagem oficial do Nginx como base
FROM nginx:stable-perl

# Remova a configuração padrão do Nginx
# RUN rm /etc/nginx/conf.d/default.conf

# Copie a configuração customizada do Nginx para o container
COPY ./srcs/requirements/certs /etc/nginx/certs

# Expõe a porta 80 para o tráfego HTTP
EXPOSE 80
EXPOSE 443
