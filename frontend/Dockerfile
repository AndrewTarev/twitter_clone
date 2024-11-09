FROM nginx:1.27

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./static /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]