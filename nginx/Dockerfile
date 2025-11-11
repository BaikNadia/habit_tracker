FROM nginx:alpine

# Копирование конфигурации nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Копирование статических файлов из Django
COPY --from=django_app /app/staticfiles /static

EXPOSE 80
