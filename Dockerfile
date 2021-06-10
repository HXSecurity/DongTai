FROM python:3.7.7
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add - \
    && apt-key fingerprint ABF5BD827BD9BF62 \
    && apt-get update -y \
    && apt install -y libc6-dev unzip vim cron swig openjdk-11-jdk

COPY requirements.txt /opt/iast/apiserver/requirements.txt
ADD https://huoqi-public.oss-cn-beijing.aliyuncs.com/iast/dongtai-models-1.0.tar.gz /opt/iast/apiserver/dongtai-models-1.0.tar.gz
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com  -r /opt/iast/apiserver/requirements.txt && pip3 install /opt/iast/apiserver/dongtai-models-1.0.tar.gz && rm -rf /opt/iast/apiserver/dongtai-models-1.0.tar.gz


COPY . /opt/iast/apiserver
WORKDIR /opt

CMD ["/usr/local/bin/uwsgi","--ini", "/opt/iast/apiserver/conf/uwsgi.ini"]
