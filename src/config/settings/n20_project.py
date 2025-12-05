from .n10_default_django import INSTALLED_APPS as DJANGO_APPS

PROJECT_APPS = ['users.apps.UsersConfig']
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS
