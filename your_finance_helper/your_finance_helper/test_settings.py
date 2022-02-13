from .settings import *
import os
from pathlib import Path

SECRET_KEY = 'django-insecure-zkp@il0+4*okay=3$8mz#rdi2ys*wnf=pl)jw7zr5ee+eeok&g'
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '176GqaT@vAf',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
