from typing import Any, final

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

from cash_register.models import Game
from cash_register.services.game import do_scan, get_game_by_gamer_name
from cash_register.types import GameDataV1


# Create your views here.
@final
class Meet(TemplateView):
    template_name = "cash_register/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        game_id = request.session.get("game_id")
        if game_id:
            return redirect("game")
        return super().get(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        name: str = request.POST["name"]
        game = get_game_by_gamer_name(name)
        request.session["name"] = name
        request.session["game_id"] = game.pk

        return redirect("game")


@final
class GameView(TemplateView):
    template_name = "cash_register/game.html"
    game: Game

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        game_id = request.session.get("game_id")
        game = Game.objects.filter(id=game_id).first()
        if not game:
            request.session.delete("game_id")
            return redirect("meet")
        self.game = game
        return super().get(request)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["game"] = self.game.data
        return kwargs


def scan_products(request: HttpRequest) -> HttpResponse:
    name: str = request.session["name"]
    game = get_game_by_gamer_name(name)
    do_scan(game)
    game_data: GameDataV1 = game.data
    return render(
        request, "cash_register/screen_amount.html", context={"game": game_data}
    )
