FROM nginx:latest

# Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Копируем основной конфиг
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем конфиг для нужной среды
ARG ENVIRONMENT=dev
COPY conf.d/default-${ENVIRONMENT}.conf /etc/nginx/conf.d/default.conf