FROM nginx:1.27

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY frontend/docker_compose/nginx.conf /etc/nginx/nginx.conf

COPY frontend/static /app/frontend/static
