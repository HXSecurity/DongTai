# DongTai-core

[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://hxsecurity.github.io/DongTaiDoc)
[![DongTai-core](https://img.shields.io/badge/DongTai--core-v1.0-lightgrey)](https://github.com/HXSecurity/dongtai-models)

[中文版本(Chinese version)](README.ZH_CN.md)

## Whit is DongTai-Core?
Provides the Django Model class that the DongTai project depends on, the Django API abstract class of the DongTai project, the vulnerability detection engine, constants, documents, etc.

## Quickstart
1. Install dongtai dependency package

Project packaging
```shell script
$ python setup.py sdist
```

Install package
```shell script
$ pip install dist/dongtai-0.1.0.tar.gz
```

2. turn on dongtai

Edit `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'dongtai',
    ...
]
```

3. turn on logger 
Edit `settings.py`, add log loggers and handlers of `dongtai-core`:
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
