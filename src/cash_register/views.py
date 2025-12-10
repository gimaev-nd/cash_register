from typing import Any, Callable, final

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View

from cash_register.models import Game
from cash_register.services.game import (
    ask_payment,
    do_scan,
    get_buyer_cash,
    get_game_by_gamer_name,
    noop,
    open_cash_register,
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
        kwargs["game"] = self.game.data
        kwargs["buyer_cash"] = get_buyer_cash(self.game)
        return kwargs


class HxGameView(View):
    template_name: str = ""
    action: Callable[[Game], None] = noop

    def post(self, request):
        name: str = request.session["name"]
        game = get_game_by_gamer_name(name)
        self.action(game)
        context = {
            "name": name,
            "game": game.data,
            "buyer_cash": get_buyer_cash(game),
        }
        print(context["buyer_cash"])
        return render(request, self.template_name, context=context)


scan_products_view = HxGameView.as_view(
    template_name="cash_register/htmx/hx_screen.html",
    action=do_scan,
)

ask_payment_view = HxGameView.as_view(
    template_name="cash_register/htmx/hx_purchase.html",
    action=ask_payment,
)

open_view = HxGameView.as_view(
    template_name="cash_register/htmx/hx_cash_register.html",
    action=open_cash_register,
)
