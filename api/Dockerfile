# Development image for the Laravel API (docs/Decisions.md D-26).
# The source is not copied in: docker-compose.yml mounts it, so edits show up without a rebuild.
FROM php:8.5-fpm-trixie

# unzip: Composer uses it to unpack packages.
# pdo_mysql: the PDO driver behind Laravel's "mariadb" connection.
RUN apt-get update \
    && apt-get install -y --no-install-recommends unzip \
    && rm -rf /var/lib/apt/lists/* \
    && docker-php-ext-install pdo_mysql

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Give www-data your host user's IDs, so files written into the mounted source (vendor/, storage/) stay yours.
ARG UID=1000
ARG GID=1000
RUN groupmod -o -g "$GID" www-data && usermod -o -u "$UID" -g "$GID" www-data

ENV COMPOSER_HOME=/tmp/composer
USER www-data
WORKDIR /var/www/html
