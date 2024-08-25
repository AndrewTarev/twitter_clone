FROM nginx

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY /frontend/static /app/frontend/static

COPY /frontend/nginx.conf /etc/nginx/nginx.conf