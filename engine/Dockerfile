FROM python:3.7.7
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add - \
    && apt-key fingerprint ABF5BD827BD9BF62 \
    && apt-get update -y \
    && apt install -y libc6-dev vim fonts-wqy-microhei

COPY requirements-prod.txt /opt/dongtai/engine/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /opt/dongtai/engine/requirements.txt

COPY . /opt/dongtai/engine
WORKDIR /opt/dongtai/engine

ENTRYPOINT ["/bin/bash","/opt/dongtai/engine/docker/entrypoint.sh"]
