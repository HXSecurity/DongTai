FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD dongtai-iast
COPY db.sql /opt/db.sql
COPY init.sh /opt/init.sh

RUN chmod u+x /opt/init.sh

CMD ["bash", "/opt/init.sh"]
