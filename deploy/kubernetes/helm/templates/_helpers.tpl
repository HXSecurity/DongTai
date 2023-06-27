{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "dongtai.name" -}}
{{- default .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "dongtai.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "dongtai.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "dongtai.labels" -}}
{{ include "dongtai.version" . }}
helm.sh/chart: {{ include "dongtai.chart" . }}
{{ include "dongtai.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{ end -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "dongtai.pv" -}}
pv.kubernetes.io/bind-completed: "yes"
pv.kubernetes.io/bound-by-controller: "yes"
{{- end -}}


{{- define "dongtai.istiolabels" -}}
sidecar.istio.io/inject: "true"
{{- end -}}

{{- define "dongtai.version" -}}
version: v1
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "dongtai.selectorLabels" -}}
app.kubernetes.io/name: {{ include "dongtai.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Values.podLabels }}
{{ toYaml .Values.podLabels }}
{{- end }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "dongtai.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- default (include "dongtai.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
{{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}


{{- define "deploy.config" -}}

{{- if .Values.lifecycle -}}
{{ include "deploy.lifecycle" . }}
{{ end -}}

{{ include "deploy.imagePullPolicy" . }}
{{ include "deploy.resources" . }}
volumeMounts:
  - name: {{ template "dongtai.fullname" . }}-configfile
    mountPath: /opt/dongtai/dongtai_conf/conf/config.ini
    subPath: config.ini
{{- if .Values.storage.persistentVolumeClaim }}
  - name: {{ template "dongtai.fullname" . }}-log-path
    mountPath: /tmp/logstash
{{- end -}}
{{- end -}}


{{- define "deploy.lifecycle" -}}
lifecycle:
  postStart:
    exec:
      command: ['/bin/bash','-c', 'sleep 60; if [ -f "/tmp/logstash/server.log" ];then mv /tmp/logstash/server.log /tmp/ ; else echo "OK!"; fi']
{{- end -}}

{{- define "deploy.configmax" -}}
{{ include "deploy.imagePullPolicy" . }}
resources:
  limits:
    cpu: 2000m
    memory: 4000Mi
  requests:
    cpu: "1000m"
    memory: 2000Mi
volumeMounts:
  - name: {{ template "dongtai.fullname" . }}-configfile
    mountPath: /opt/dongtai/dongtai_conf/conf/config.ini
    subPath: config.ini
{{- if .Values.storage.persistentVolumeClaim }}
  - name: {{ template "dongtai.fullname" . }}-log-path
    mountPath: /tmp/logstash
{{- end -}}
{{- end -}}
{{- define "deploy.imagePullPolicy" -}}
imagePullPolicy: {{.Values.imagePullPolicy}}
{{- end -}}

{{- define "deploy.initContainers" -}}
initContainers:
  - image: {{ .Values.images }}/dongtai-logrotate:{{ .Values.tag }}
    command:
    - sh
    - -c
    - echo {{.Values.somaxconn}} > /proc/sys/net/core/somaxconn
    imagePullPolicy: Always
    name: setsysctl
    securityContext:
      privileged: true
{{- end -}}


{{- define "deploy.resources" -}}
resources:
  limits:
    cpu: {{.Values.cpu}}
    memory: {{.Values.memory}}
  requests:
    cpu: {{.Values.cpu}}
    memory: {{.Values.memory}}
{{- end -}}
{{- define "deploy.config.vo" -}}
volumes:
  - name: {{ template "dongtai.fullname" . }}-configfile
    configMap:
      name: dongtai-iast-config.ini
{{- if .Values.storage.persistentVolumeClaim }}
  - name: {{ template "dongtai.fullname" . }}-log-path
    persistentVolumeClaim:
      {{ include "deploy.config.persistentVolumeClaim" . }}
{{- end -}}
{{- end -}}

{{- define "deploy.config.persistentVolumeClaim" -}}
claimName: {{.Values.storage.persistentVolumeClaim}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}

{{- define "config.ini" -}}
    [mysql]
    host = {{.Values.mysql.host}}
    port = {{.Values.mysql.port}}
    name = {{.Values.mysql.name}}
    user = {{.Values.mysql.user}}
    password = {{.Values.mysql.password}}

    [redis]
    host = {{.Values.redis.host}}
    port = {{.Values.redis.port}}
    password = {{.Values.redis.password}}
    db = {{.Values.redis.db}}

    [engine]
    url = http://dongtai-engine:8000

    [apiserver]
    url = http://dongtai-server:8000

    [security]
    csrf_trust_origins = {{.Values.csrfTrustOrigins}}
    secret_key = {{.Values.secretKey}}

    [smtp]
    server = {{.Values.smtp.server}}
    user = {{.Values.smtp.user}}
    password = {{.Values.smtp.password}}
    from_addr = {{.Values.smtp.from_addr}}
    ssl = {{.Values.smtp.ssl}}
    cc_addr = {{.Values.smtp.cc_addr}}
    port = {{.Values.smtp.port}}

    [sca]
    base_url = {{.Values.sca.sca_url}}
    timeout = 5
    token = {{.Values.sca.sca_token}}

    [task]
    retryable = true
    max_retries = 3
    async_send = true
    async_send_delay = 5

    [log_service]
    host = dongtai-logstash-svc
    port = 8083

    [common_file_path]
    tmp_path = /tmp/logstash
    report_img = report/img
    report_pdf = report/pdf
    report_word = report/word
    report_excel = report/excel

    [elastic_search]
    enable = false
    host = http://user:passwd@127.0.0.1:9200
    vulnerability_index = dongtai-iast-alias-dongtai-v1-vulnerability
    asset_aggr_index = dongtai-iast-alias-dongtai-v1-asset-aggr
    asset_index = dongtai-iast-alias-dongtai-v1-asset
    method_pool_index = dongtai-iast-alias-dongtai-v1-method-pool
    asset_vul_index = dongtai-iast-alias-dongtai-v1-asset-vul

    [other]
    logging_level = {{.Values.logging_level}}
    cache_preheat = True
    domain_vul = {{.Values.Dongtai_url}}
    dast_token = {{.Values.usb.usb_token}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "nginx.conf" -}}
    worker_processes  auto;
    events {
        worker_connections  65535;
    }
    http {
        include       mime.types;
        default_type  application/octet-stream;
        sendfile        on;
        keepalive_timeout  65;
        #gzip  on;
        gzip on;
        gzip_min_length  5k;
        gzip_buffers     4 16k;
        #gzip_http_version 1.0;
        gzip_comp_level 3;
        gzip_types text/plain application/javascript application/x-javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png;
        gzip_vary on;
        server {
            listen  80;
            server_name 0.0.0.0;
            client_max_body_size 100M;
            location / {
                root /usr/share/nginx/html;   #站点目录
                index index.html index.htm;   #添加属性。
                try_files $uri $uri/ /index.html;
            }
            location /api/ {
              proxy_read_timeout 60;
              proxy_pass http://dongtai-server-svc:80/api/;
            }
            location /upload/ {
              proxy_pass http://dongtai-server-svc:80/upload/;
            }
            location /openapi/ {
             proxy_set_header X-real-ip $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header User-Agent $http_user_agent;
             proxy_set_header X-Host $http_x_forwarded_host;
             proxy_read_timeout 60;
             proxy_pass http://dongtai-server-svc:80/;
            }
            location /log/ {
             proxy_pass http://dongtai-logstash-svc:8082/;
            }
            location = /50x.html {
                root   /usr/share/nginx/html;
            }
        }
    }
{{- end -}}

