FROM python:3.10-slim
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN apt-get update -y \
    && apt install -y gettext gcc make cmake libmariadb-dev curl libc6-dev unzip cron \
    fonts-wqy-microhei vim build-essential ninja-build cython3 pybind11-dev libre2-dev locales \
#   htop sysstat net-tools iproute2 procps lsof \
    openjdk-11-jdk \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen \
    && ALIMARCH=`arch` && curl -L https://charts.dongtai.io/apk/${ALIMARCH}/wkhtmltopdf -o /usr/bin/wkhtmltopdf \
    && chmod +x /usr/bin/wkhtmltopdf

COPY Pipfile .
COPY Pipfile.lock .
#RUN pip install -U pip && pip install pipenv wheel && python3 -m pipenv sync --system -v

COPY . /opt/dongtai
WORKDIR /opt/dongtai

RUN /bin/bash -c 'mkdir -p /tmp/{logstash/{batchagent,report/{img,word,pdf,excel,html}},iast_cache/package}' \
    && mv /opt/dongtai/*.jar /tmp/iast_cache/package/ || true && mv /opt/dongtai/*.tar.gz /tmp/ || true 
ENTRYPOINT ["/bin/bash","/opt/dongtai/deploy/docker/entrypoint.sh"]
