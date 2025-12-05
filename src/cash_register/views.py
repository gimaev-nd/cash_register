from typing import final

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from cash_register.services.game import get_game_by_gamer_name


# Create your views here.
@final
class Meet(TemplateView):
    template_name = "cash_register/index.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        name: str = request.POST["name"]
        game = get_game_by_gamer_name(name)
        request.session["name"] = name
        request.session["game_id"] = game.pk

        return redirect("game")


@final
class Game(TemplateView):
    template_name = "cash_register/game.html"

