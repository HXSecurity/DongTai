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

## How to contribute code？

### Development

- Use docker-compose (recommended)
- Use batect (in the experimental stage, it will be recommended after the jdk dependency is removed)
- Use local environment

Tip: Avoid using methods other than the first two, which can not only reduce the time to configure the local development environment, but also reduce test errors, compatibility errors, etc. caused by the difference between the development environment and the distribution environment.

#### Develop with docker-compose(recommend)

1. Initialize the environment
````
cp config.ini.example config.ini
````

2. Start the project with docker-compose

````
docker-compose -p dongtai-iast-dev up -d
````
This command will build the webapi image in the current directory and pull the minimum required image in the hole state IAST. In addition to the `dongtai-webapi` built based on the current directory, it also includes `dongtai-openapi`, `dongtai-web`, `dongtai-mysql`, `dongtai-redis` images.

If full service is required, use the following command

```
docker-compose -p dongtai-iast-dev up -d --scale dongtai-engine=1  --scale dongtai-engine-task=1
```

Among them, `dongtai-mysql` exposes port 33060 to facilitate developers to link mysql from the outside, while `dongtai-webapi` additionally exposes port 8010, which is convenient for developers to debug using methods other than uwsgi startup, such as `python manage.py runserver 0.0.0.0:8000`.

3. After modifying the code
Use the following command to restart the webapi service, the service will start with the modified code
````
docker-compose -p dongtai-iast-dev restart dongtai-webapi
````

If you have modified deployment-related content, please use the following command to rebuild the image
````
docker-compose -p dongtai-iast-dev up -d --build
````

4. Extra

If you want to use [python-agent](https://github.com/HXSecurity/DongTai-agent-python) for security detection during development, this has been reserved in docker-compose and code.

a. Apply for an account at [DongTai IAST-Account Registration](https://jinshuju.net/f/I9PNmf?from=webapi)

b. Download the dongtai-python-agent.tar.gz it belongs to and place it in the current directory of webapi

c. Execute the following command and cancel `- PYTHONAGENT=TRUE` in docker-compose.yml

````
docker exec -it dongtai-iast-dev_dongtai-webapi_1 pip install dongtai-agent-python.tar.gz
````

d. Use the command in 3. to restart the service

#### Use batect

1. Run `./batect` to check whether the dependencies are satisfied, and initialize the batect.

2. Run `./batect --list-tasks` to view the existing tasks, as follows:

```
integration:
- integration-test-all: integration with all components
- integration-test-web: integration with web front-end

serve:
- serve: Serve the webapi application standingalone
- serve-with-db: Serve the webapi application with db

test:
- test: run webapi unittest
```

For example:
Running the following command will build webapi container and db container.
```
./batect serve-with-db
```
The following environment variables can be used.

- DOC: ${WEBAPI_DOC:-TRUE}
- debug: ${WEBAPI_debug:-true}
- SAVEEYE: ${WEBAPI_SAVEEYE:-TRUE}
- REQUESTLOG: ${WEBAPI_REQUESTLOG:-TRUE}
- CPROFILE: ${WEBAPI_CPROFILE:-TRUE}
- PYTHONAGENT: ${WEBAPI_PYTHON_AGENT:-FALSE}
- PROJECT_NAME: ${WEBAPI_PROJECT_NAME:-LocalWEBAPI}
- PROJECT_VERSION: ${WEBAPI_PROJECT_VERSION:-v1.0}
- LOG_PATH: ${WEBAPI_LOG_PATH:-/tmp/dongtai-agent-python.log}
- DONGTAI_IAST_BASE_URL: ${DONGTAI_IAST_BASE_URL:-https://iast.io/openapi}
- DONGTAI_AGNET_TOKEN: ${DONGTAI_AGNET_TOKEN:-79798299b48839c84886d728958a8f708e119868}

example:
Use the host environment variable to override the default, enabling PYTHONAGENT:
```
WEBAPI_PYTHON_AGENT=TRUE ./batect serve-with-db
```

[Batect Installation](https://batect.dev/docs/getting-started/installation)
[Batect Tutorial](https://batect.dev/docs/getting-started/tutorial)

#### Use local environment

1. Install the required dependencies

```
python -m pip install -r requirements-test.txt
```

Note: jq cannot be installed under windows, jq is used to process json parsing of sensitive information, if it is not develop related functions, it can be ignored, or WSL is used for development under windows


2. Initialize the database


- Pull the database mirror corresponding to the version and start the mirror
```
docker pull dongtai/dongtai-mysql:latest
docker run -itd --name dongtai-mysql -p 3306:3306 dongtai/dongtai-mysql:latest
```

If you need to create or modify the database table, please refer to the [DongTai-Base-Image](https://github.com/HXSecurity/Dongtai-Base-Image) specification and submit the relevant modified .sql file


3. Modify the configuration file

- Copy the configuration file `conf/config.ini.example` to `conf/config.ini` and change the configuration; among them, the url corresponding to `engine` is the service address of `DongTai-engine`, and `apiserver` corresponds to The url is the service address of `DongTai-openapi`
- You can leave out engine and apiserver when you only develop webapi-related functions

4. Run service debugging

- Development related environment variables

`PYTHONAGENT=TRUE` Open pythonagent, need to be installed manually, refer to [Python Agent Installation](http://doc.dongtai.io/02_start/03_agent.html#python-agent)

`DOC=TRUE` Open swagger path is `/api/XZPcGFKoxYXScwGjQtJx8u/schema/swagger-ui/`

`debug=true` enable debug mode

- Run `python manage.py runserver` to start the service 


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


## Deploy

- Use the tools provided in [DongTai](https://github.com/HXSecurity/DongTai) (recommended)
- Docker deployment
- Source code deployment

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


**Source code deployment**

1.Install the required dependencies

```
python -m pip install -r requirements-prod.txt
```

2.Initialize the database

- Install MySql 5.7, create the database `DongTai-webapi`, and run the database file `conf/db.sql`
- Enter the `webapi` directory and run the `python manage.py createsuperuser` command to create an administrator

OR use docker way to host a database

- Pull the corresponding database images and run it
```
docker pull  dongtai/dongtai-mysql:latest 
docker run -itd --name dongtai-mysql -p 3306:3306 dongtai/dongtai-mysql:latest 
```



3.Modify the configuration file

- Copy the configuration file `conf/config.ini.example` to `conf/config.ini` and change the configuration; the url corresponding to `engine` is the service address of` DongTai-engine`, and the url corresponding to `apiserver` is the service address of `DongTai-openapi`

4.Run the service

- Run `python manage.py runserver` to start the service



### More resources
- [Documentation](https://doc.dongtai.io/)
- [DongTai WebSite](https://iast.io)

<img src="https://static.scarf.sh/a.png?x-pxid=44779bf0-9262-4801-bb88-4a36ee0fdcfe" />
