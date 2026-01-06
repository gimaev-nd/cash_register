from itertools import combinations
from typing import Any, NamedTuple

import pytest
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.urls import reverse
from django.views.generic.base import View

from cash_register.models import Game
from cash_register.types import Page
from cash_register.views import GameMixin

pytestmark = pytest.mark.django_db


class FakeRequest(NamedTuple):
    META: dict[str, str] = {}
    method: str = "GET"
    session: dict[str, Any] = {}
    path: str = "/"


class GameView(GameMixin, View):
    def commont_method(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
        return HttpResponse("ok")

    get = post = commont_method


class TestGameMixin:
    def test_game_mixin_welcome(self):
        request = FakeRequest()
        view = GameView.as_view(page="abc")

        response = view(request)

        assert response.status_code == 302
        assert response.headers["Location"] == "/"

    def test_game_mixin_method_post(self):
        request = FakeRequest(method="POST")
        view = GameView.as_view(page="")

        response = view(request)

        assert response.status_code == 200

    def set_page(self, game: Game, page: Page):
        game_data = game.get_game_data()
        game_data.page = page
        game.set_game_data(game_data)

    @pytest.mark.parametrize("view_page,game_page", combinations(Page, 2))
    def test_game_mixin_redirect_to_page(
        self, game: Game, view_page: Page, game_page: Page
    ):
        self.set_page(game, game_page)
        request = FakeRequest(session={"name": "Вася", "game_id": 1})
        view = GameView.as_view(page=view_page)

        response = view(request)

        assert response.status_code == 302
        assert response.headers["Location"] == reverse(game_page.view_name)

    @pytest.mark.parametrize("page", Page)
    def test_game_mixin_same_page(self, game: Game, page: Page):
        self.set_page(game, page)
        request = FakeRequest(session={"name": "Вася", "game_id": 1})
        view = GameView.as_view(page=page)

        response = view(request)

        assert response.status_code == 200
