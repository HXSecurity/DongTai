# DongTai-core

[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://hxsecurity.github.io/DongTaiDoc)
[![DongTai-core](https://img.shields.io/github/v/release/HXSecurity/Dongtai-core?label=Dongtai-core)](https://github.com/HXSecurity/DongTai-core/releases)

## 项目介绍
提供DongTai项目依赖的Django Model对象，DongTai项目的Django API抽象类、漏洞检测引擎、常量、文档等内容。

## 快速开始
1. 安装dongtai依赖包

项目打包
```shell script
$ python setup.py sdist
```

安装dongtai包
```shell script
$ pip install dist/dongtai-0.1.0.tar.gz
```

2. 快速开始

在`settings.py`:
```python
INSTALLED_APPS = [
    ...
    'dongtai',
    ...
]
```

3. 打开日志
在`settings.py`中，增加`dongtai-core`的日志loggers及handlers:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} [{module}.{funcName}:{lineno}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'dongtai.core': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/core.log',
            'backupCount': 5,
            'maxBytes': 1024 * 1024 * 10,
            'formatter': 'verbose'
        },
    },
    'loggers': 
        ...
        'dongtai-core': {
            'handlers': ['console', 'dongtai.core'],
            'propagate': True,
            'level': 'INFO',
        },
        ...
    }
}
```
