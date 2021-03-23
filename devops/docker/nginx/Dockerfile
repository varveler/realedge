FROM tutum/nginx

# install git
RUN  apt-get update && apt-get install -y git

# install nano
RUN  apt-get update && apt-get install -y nano

RUN cd /var \
    && mkdir -p www/certbot \
    && chgrp www-data www/certbot

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN rm /etc/nginx/sites-enabled/default

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

ADD sites-enabled/ /etc/nginx/sites-enabled
ENV TERM xterm
