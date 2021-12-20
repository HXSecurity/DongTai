# DongTai-webapi
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://github.com/HXSecurity/DongTai)
[![DongTai-webapi](https://img.shields.io/github/v/release/HXSecurity/Dongtai-webapi?label=Dongtai-webapi)](https://github.com/HXSecurity/DongTai-webapi/releases)
[![Release DongTai WebApi](https://github.com/HXSecurity/DongTai-webapi/actions/workflows/release_webapi.yml/badge.svg)](https://github.com/HXSecurity/DongTai-webapi/actions/workflows/release_webapi.yml)

[中文版本(Chinese version)](README.ZH_CN.md)

## Whit is DongTai-WebApi?
DongTai-WebAPI is used to user resource management ,including:


- Project management
- Vulnerability management
- User data retrieval
- System resources configuration
- User/role management
- Agent deployment management
- Tenant management
- Deployment document retrieval



## Deploy
- Source code deployment
- Docker deployment

**Source code deployment**

1.Install the required dependencies

```
python -m pip install -r requirements-test.txt
```

2.Initialize the database

- Install MySql 5.7, create the database `DongTai-webapi`, and run the database file `conf/db.sql`
- Enter the `webapi` directory and run the `python manage.py createsuperuser` command to create an administrator

OR use docker way to host a database

- Pull the corresponding database images and run it
```
docker pull  registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest 
docker run -itd --name dongtai-mysql -p 3306:3306 registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest 
```



3.Modify the configuration file

- Copy the configuration file `conf/config.ini.example` to `conf/config.ini` and change the configuration; the url corresponding to `engine` is the service address of` DongTai-engine`, and the url corresponding to `apiserver` is the service address of `DongTai-openapi`

4.Run the service

- Run `python manage.py runserver` to start the service


**Container deployment**

1.Initialize the database

- Pull the corresponding database images and run it

```
docker pull  registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest 
docker run -itd --name dongtai-mysql -p 3306:3306 registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest 
```

2. Modify the configuration file

Copy the configuration file `conf/config.ini.example` to `conf/config.ini` and change the configuration; among them:
- The URL corresponding to the `engine` is the service address of `DongTai-engine`
- The url corresponding to `apiserver` is the service address of `DongTai-openapi`

3.Build the image
```
$ docker build -t huoxian/dongtai-webapi:latest .
```

4.Start the container
```
$ docker run -d -p 8000:8000 --restart=always --name dongtai-webapi huoxian/dongtai-webapi:latest
```
### Document

- API documentation corresponding to the project 

1. Add document-related parameters when starting the container :
```
$ docker run -d -p 8000:8000 --restart=always -e environment=DOC --name dongtai-webapi huoxian/dongtai-webapi:latest
```
Here you need to start the corresponding mysql database. If you only want to start the webapi project to view the document, you need to add the following parameter `-e database=sqlite` (only start the webapi project to view the document, and does not guarantee the compatibility under sqlite ), the complete command is:
```
$ docker run -d -p 8000:8000 --restart=always -e environment=DOC -e database=sqlite --name dongtai-webapi huoxian/dongtai-webapi:latest
```

2. Access the corresponding API in the container:

Swagger-ui address is `http://<containerip:port>/api/XZPcGFKoxYXScwGjQtJx8u/schema/swagger-ui/#/`

The Redoc address is `http://<containerip:port>/api/XZPcGFKoxYXScwGjQtJx8u/schema/redoc/`

If you need to separately export swagger.json
The address is `http://<containerip:port>/api/XZPcGFKoxYXScwGjQtJx8u/schema/`

3. The specific API authentication mode has been included in the API document, and the corresponding token can be found on the installation agent part of the web.

### More resources
- [Documentation](https://doc.dongtai.io/)
- [DongTai WebSite](https://iast.io)

<img src="https://static.scarf.sh/a.png?x-pxid=44779bf0-9262-4801-bb88-4a36ee0fdcfe" />
