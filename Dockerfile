FROM python:3.7-slim
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN apt-get update -y \
    && apt install -y gettext gcc make cmake libmariadb-dev curl libc6-dev unzip cron  openjdk-11-jdk fonts-wqy-microhei vim
#     htop sysstat net-tools iproute2 procps lsof
    
RUN curl -L https://github.com/Endava/cats/releases/download/cats-7.0.1/cats-linux -o  /usr/local/bin/cats \
    && chmod +x /usr/local/bin/cats \
    && ln -s /usr/local/bin/cats /usr/bin/cats \
    && curl -L https://huoqi-public.oss-cn-beijing.aliyuncs.com/iast/wkhtmltopdf -o /usr/local/bin/wkhtmltopdf \
    && chmod +x /usr/local/bin/wkhtmltopdf \
    && ln -s  /usr/local/bin/wkhtmltopdf /usr/bin/wkhtmltopdf


COPY requirements-prod.txt /opt/dongtai/webapi/requirements.txt
RUN pip3 install -r /opt/dongtai/webapi/requirements.txt

# debug performance ...
COPY . /opt/dongtai
WORKDIR /opt/dongtai

RUN /bin/bash -c 'mkdir -p /tmp/{logstash/{batchagent,report/{img,word,pdf,excel,html}},iast_cache/package}' && mv /opt/dongtai/*.jar /tmp/iast_cache/package/ || true && mv /opt/dongtai/*.tar.gz /tmp/ || true 
ENTRYPOINT ["/bin/bash","/opt/dongtai/deploy/docker/entrypoint.sh"]