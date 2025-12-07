from pathlib import Path

from .n10_default_django import INSTALLED_APPS as DJANGO_APPS

BASE_DIR = Path(__file__).resolve().parents[2]
PROJECT_APPS = [
    "users.apps.UsersConfig",
    "cash_register.apps.CashRegisterConfig",
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS
STATIC_ROOT = BASE_DIR / "staticfiles"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
