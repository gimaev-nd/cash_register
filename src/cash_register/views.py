from typing import Any, Callable, final

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View

from cash_register.models import Game
from cash_register.services.game import (
    ask_payment,
    do_scan,
    get_game_by_gamer_name,
    noop,
    open_cash_register,
    take_cashe,
)


# Create your views here.
@final
class Meet(TemplateView):
    template_name = "cash_register/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        game_id = request.session.get("game_id")
        if game_id:
            return redirect("game")
        if True:
            _ = self.create_game(request, "Наиль")
            return redirect("game")
        return super().get(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        name: str = request.POST["name"]
        game = get_game_by_gamer_name(name)
        request.session["name"] = name
        request.session["game_id"] = game.pk

        return redirect("game")

    def create_game(self, request: HttpRequest, name: str) -> Game:
        game = get_game_by_gamer_name(name)
        request.session["name"] = name
        request.session["game_id"] = game.pk
        return game


@final
class GameView(TemplateView):
    template_name = "cash_register/game.html"
    game: Game

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        game_id: int | None = request.session.get("game_id")
        if game_id is None:
            return redirect("meet")
        game = Game.objects.filter(id=game_id).first()
        if not game:
            request.session.delete("game_id")
            return redirect("meet")
        self.game = game
        return super().get(request)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["game"] = self.game.get_game_data()
        return kwargs


class HxGameView(View):
    template_name: str = "cash_register/htmx/hx_game.html"
    action: Callable[[Game], None] = noop

    def post(self, request) -> HttpResponse:
        name: str = request.session["name"]
        game = get_game_by_gamer_name(name)
        self.action(game)
        context = {
            "name": name,
            "game": game.get_game_data(),
        }
        return render(request, self.template_name, context=context)


scan_products_view = HxGameView.as_view(action=do_scan)
ask_payment_view = HxGameView.as_view(action=ask_payment)
open_view = HxGameView.as_view(action=open_cash_register)
take_cashe_view = HxGameView.as_view(action=take_cashe)
