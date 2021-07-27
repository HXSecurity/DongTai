FROM python:3.7.7
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add - \
    && apt-key fingerprint ABF5BD827BD9BF62 \
    && apt-get update -y \
    && apt install -y libc6-dev unzip vim cron swig openjdk-11-jdk

COPY requirements-prod.txt /opt/dongtai/openapi/requirements.txt
RUN pip3 install -r /opt/dongtai/openapi/requirements.txt


COPY . /opt/dongtai/openapi
WORKDIR /opt/dongtai/openapi

CMD ["/usr/local/bin/uwsgi","--ini", "/opt/dongtai/openapi/conf/uwsgi.ini"]
