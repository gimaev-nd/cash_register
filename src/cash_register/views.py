from typing import TYPE_CHECKING, Any, Callable, cast, final

from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View

from cash_register.models import Game
from cash_register.services.game import (
    ask_payment,
    check,
    do_scan,
    get_game_by_gamer_name,
    move_cash,
    move_cash_up,
    noop,
    open_cash_register,
    take_cashe,
)
from cash_register.types import CashName, Nominal, Page


class GameMixin(View if TYPE_CHECKING else object):
    page: Page = Page.WELCOME

    def __init__(self, *args, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.game: Game | None = None
        self.gamer_name: str | None = None

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
        print("!" * 8, [*request.META])
        if request.method != "GET":
            return super().dispatch(request, *args, **kwargs)
        page = self.page
        if "name" not in request.session or "game_id" not in request.session:
            page = Page.WELCOME
            if page != self.page:
                return redirect(page.view_name)
        self.gamer_name = request.session.get("name")

        if page == self.page:
            return super().dispatch(request, *args, **kwargs)
        return redirect(page.view_name)

    def create_game(self, request: HttpRequest, name: str) -> Game:
        game = get_game_by_gamer_name(name)
        request.session["name"] = name
        request.session["game_id"] = game.pk
        return game


# Create your views here.
@final
class Meet(GameMixin, TemplateView):
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
    template_name = "cash_register/game_page.html"
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

    def post(self, request: HttpRequest) -> HttpResponse:
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
check_view = HxGameView.as_view(action=check)
# up_view = HxGameView.as_view(action=up)


class HxMoveCacheView(View):
    template_name: str = "cash_register/htmx/hx_game.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        name = cast(str, request.session["name"])
        cash_src = CashName(request.POST["cash_src"])
        cash_dst = CashName(request.POST["cash_dst"])
        nominal = Nominal(int(request.POST["nominal"]))
        game = get_game_by_gamer_name(name)
        move_cash(game, cash_src, cash_dst, nominal)
        context = {
            "name": name,
            "game": game.get_game_data(),
        }
        return render(request, self.template_name, context=context)


class HxMoveCacheUpView(View):
    template_name: str = "cash_register/htmx/hx_game.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        name = cast(str, request.session["name"])
        cash_src = CashName(request.POST["cash_src"])
        nominal = Nominal(int(request.POST["nominal"]))
        game = get_game_by_gamer_name(name)
        move_cash_up(game, cash_src, nominal)
        context = {
            "name": name,
            "game": game.get_game_data(),
        }
        return render(request, self.template_name, context=context)
