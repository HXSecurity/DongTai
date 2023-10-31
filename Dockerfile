FROM python:3.10-slim-bullseye
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN apt-get update -y \
  && apt install -y gettext gcc make cmake libmariadb-dev curl libc6-dev libxrender1 libxtst6 libxi6 unzip cron \
  fonts-wqy-microhei vim build-essential ninja-build cython3 pybind11-dev libre2-dev locales \
  libsasl2-dev python3-dev libldap2-dev libssl-dev \
  # htop sysstat net-tools iproute2 procps lsof \
  zip libjpeg62 \
  && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen \
  && ALIMARCH=`arch` && curl -L https://charts.dongtai.io/apk/${ALIMARCH}/wkhtmltopdf -o /usr/bin/wkhtmltopdf \
  && chmod +x /usr/bin/wkhtmltopdf \
  && if [ "aarch64" = "$ALIMARCH" ] ; then curl -L https://github.com/HXSecurity/tantivy-py/releases/download/0.21.0/tantivy-0.20.1-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl -o /tmp/tantivy-0.20.1-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl; \
  && else curl -L https://github.com/HXSecurity/tantivy-py/releases/download/0.21.0/tantivy-0.20.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl -o /tmp/tantivy-0.20.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl; fi

COPY Pipfile .
COPY Pipfile.lock .
RUN pip install -U pip && pip install pipenv wheel && python3 -m pipenv sync --system -v
RUN ALIMARCH=`arch` && if [ "aarch64" = "$ALIMARCH" ] ; then pip install /tmp/tantivy-0.20.1-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl; else pip install /tmp/tantivy-0.20.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl; fi

COPY . /opt/dongtai
WORKDIR /opt/dongtai

RUN /bin/bash -c 'mkdir -p /tmp/{logstash/{batchagent,report/{img,word,pdf,excel,html}},iast_cache/package}' \
  && mv /opt/dongtai/*.jar /tmp/iast_cache/package/ || true && mv /opt/dongtai/*.tar.gz /tmp/ || true 
ENTRYPOINT ["/bin/bash","/opt/dongtai/deploy/docker/entrypoint.sh"]
