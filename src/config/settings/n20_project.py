from pathlib import Path

from .n10_default_django import INSTALLED_APPS as DJANGO_APPS

BASE_DIR = Path(__file__).resolve().parents[3]
PROJECT_APPS = [
    "users.apps.UsersConfig",
    "cash_register.apps.CashRegisterConfig",
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS
