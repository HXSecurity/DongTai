FROM python:3.7.7
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add - \
    && apt-key fingerprint ABF5BD827BD9BF62 \
    && apt-get update -y \
    && apt install -y libc6-dev unzip  vim cron swig

ADD https://huoqi-public.oss-cn-beijing.aliyuncs.com/iast/dongtai-models-1.0.tar.gz /opt/iast/webapi/dongtai-models-1.0.tar.gz
COPY requirements.txt /opt/iast/webapi/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /opt/iast/webapi/requirements.txt  && pip3 install /opt/iast/webapi/dongtai-models-1.0.tar.gz && rm -rf /opt/iast/webapi/dongtai-models-1.0.tar.gz

COPY . /opt/iast/webapi
WORKDIR /opt

CMD ["/usr/local/bin/uwsgi","--ini", "/opt/iast/webapi/conf/fire_uwsgi.ini"]
