FROM nginx:alpine
<<<<<<< HEAD

# Копирование конфигурации nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Копирование статических файлов из Django
COPY --from=django_app /app/staticfiles /static

EXPOSE 80
=======
COPY nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
>>>>>>> server-changes
