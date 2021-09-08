# DongTai-webapi
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://huoxianclub.github.io/LingZhi/)
[![DongTai--webapi](https://img.shields.io/badge/DongTai--webapi-v1.0.0-lightgrey)](https://huoxianclub.github.io/LingZhi/#/doc/tutorial/quickstart)
[![Deploy DongTai WebApi To AWS](https://github.com/HXSecurity/DongTai-webapi/actions/workflows/deploy_webapi_to_aws.yml/badge.svg)](https://github.com/HXSecurity/DongTai-webapi/actions/workflows/deploy_webapi_to_aws.yml)

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

1.Initialize the database

- Install MySql 5.7, create the database `DongTai-webapi`, and run the database file `conf/db.sql`
- Enter the `webapi` directory and run the `python manage.py createsuperuser` command to create an administrator

2.Modify the configuration file

- Copy the configuration file `conf/config.ini.example` to `conf/config.ini` and change the configuration; the url corresponding to `engine` is the service address of` DongTai-engine`, and the url corresponding to `apiserver` is the service address of `DongTai-openapi`

3.Run the service

- Run `python manage.py runserver` to start the service


**Container deployment**

1.Initialize the database

- Install MySql 5.7, create the database `DongTai-webapi`, and run the database file `conf/db.sql`
- Enter the `webapi` directory and run the `python manage.py createsuperuser` command to create an administrator

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

### More resources
- [Documentation](https://hxsecurity.github.io/DongTai-Doc/#/)
- [DongTai WebSite](http://iast.io)
