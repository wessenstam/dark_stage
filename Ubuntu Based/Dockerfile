#Download base image ubuntu 16.04
FROM ubuntu:16.04
 
# Update Software repository
RUN apt-get update
 
# Install nginx, php-fpm and supervisord from ubuntu repository
RUN apt-get install -y nginx php7.0-fpm supervisor git sshpass sudo && \
    rm -rf /var/lib/apt/lists/*
 
#Define the ENV variable
ENV nginx_vhost /etc/nginx/sites-available/default
ENV php_conf /etc/php/7.0/fpm/php.ini
ENV nginx_conf /etc/nginx/nginx.conf
ENV supervisor_conf /etc/supervisor/supervisord.conf
 
# Enable php-fpm on nginx virtualhost configuration
COPY default ${nginx_vhost}
RUN sed -i -e 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/g' ${php_conf} && \
    echo "\ndaemon off;" >> ${nginx_conf}
 
#Copy supervisor configuration
COPY config/supervisord.conf ${supervisor_conf}
 
RUN mkdir -p /run/php && \
    chown -R www-data:www-data /var/www/html && \
    chown -R www-data:www-data /run/php

# Change the autoindex for NGINX for the images directory
RUN sed -i 's/=404;/=404;\n\tautoindex on;/g' ${nginx_vhost}

# Grab the nutanixworkshop/stageworkshop github
RUN cd /opt && git clone https://github.com/jncox/stageworkshop.git

# Make the directory for the images
RUN mkdir /images
RUN ln -s /images /var/www/html/images
RUN echo "www-data ALL=(ALL) NOPASSWD:ALL >> /etc/sudoers"

# Copy the index.php into the right location
COPY ../webpages/index.php /var/www/html

# Change the nginx.conf so it runs index.php by default
RUN sed -i -e 's/index on;/index on;\n\tindex index.php index.html index.htm;\n/g' ${nginx_vhost} 


# Volume configuration. This needs to be where we have the files needed (server.txt and which workshop)
VOLUME ["/var/www/html","/images"]

# Copy the start and stop scripts
COPY config/start.sh /start.sh
COPY config/stop.sh /stop.sh
RUN chmod +x /start.sh
RUN chmod +x /stop.sh
CMD ["/bin/bash","/start.sh"]

 
# Configure Services and Port
 
EXPOSE 80 443