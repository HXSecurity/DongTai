FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD dongtai-iast

# ADD http://oss.huoxian.cn/sca.sql /opt/sca.sql
ADD sca.sql /opt/sca.sql
# ADD http://oss.huoxian.cn/rule.sql /opt/rule.sql
ADD rule.sql /opt/rule.sql
COPY db.sql /opt/db.sql
COPY init.sh /opt/init.sh

RUN chmod u+x /opt/init.sh

CMD ["bash", "/opt/init.sh"]
