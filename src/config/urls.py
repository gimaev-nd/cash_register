"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from cash_register import views as cash_register_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", cash_register_views.Meet.as_view(), name="meet"),
    path("game/", cash_register_views.GameView.as_view(), name="game"),
    path("scan/", cash_register_views.scan_products_view, name="scan"),
    path("ask_payment/", cash_register_views.ask_payment_view, name="ask_payment"),
    path("open/", cash_register_views.open_view, name="open"),
    path("take/", cash_register_views.take_cashe_view, name="take_cashe"),
    path("check/", cash_register_views.check_view, name="check"),
    path("move_cash/", cash_register_views.HxMoveCacheView.as_view(), name="move_cash"),
    path("new_level/", cash_register_views.HxMoveCacheView.as_view(), name="new_level"),
    path("history/", cash_register_views.HxMoveCacheView.as_view(), name="history"),
]
