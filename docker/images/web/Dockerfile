FROM php:7.2-apache

RUN apt-get update && apt-get install -y \
        curl \
        wget \
        git \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libmcrypt-dev \
        libpng-dev \
        libicu-dev \
    && pecl install mcrypt-1.0.1 \
    && docker-php-ext-install -j$(nproc) iconv mbstring mysqli pdo_mysql zip \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) gd \
    && docker-php-ext-enable mcrypt \
    && docker-php-ext-configure intl \
    && docker-php-ext-install intl

#Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

ADD php.ini /usr/local/etc/php/php.ini

RUN a2enmod rewrite headers

RUN chown -R www-data:www-data /var/www/hrbank.ga/vendor/ && chown -R www-data:www-data /var/www/hrbank.ga/storage/
RUN chown -R www-data:www-data php /var/www/hrbank.ga/artisan key:generate

WORKDIR /var/www

#CMD ["php-fpm"]