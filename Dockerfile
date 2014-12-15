FROM tozd/runit

EXPOSE 27017/tcp
EXPOSE 5432/tcp

RUN apt-get update -q -q
RUN echo locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8 | debconf-set-selections
RUN echo locales locales/default_environment_locale select en_US.UTF-8 | debconf-set-selections
RUN apt-get install curl mongodb postgresql postgresql-server-dev-9.3 python-pip --yes --force-yes
RUN echo "listen_addresses = '*'" >> /etc/postgresql/9.3/main/postgresql.conf
RUN echo 'hostssl all all 0.0.0.0/0 md5' >> /etc/postgresql/9.3/main/pg_hba.conf
RUN curl https://install.meteor.com | /bin/sh

COPY ./etc /etc
