# from pytest_bdd import scenario, given, when, then
from django.urls import reverse
from pytest_bdd import parsers, scenarios, then, when

scenarios("anonymous_user_on_home_page.feature", "login.feature")


@when(parsers.parse("{username} входит на {page}"), target_fixture="opened_page")
@when(parsers.parse("{username} открывает {page}"), target_fixture="opened_page")
def open_page(username, page, client):
    if username != "неизвестный пользователь":
        client.session["name"] = username
    if page == "главную страницу":
        url = reverse("meet")
    else:
        assert False, "Тест не должен попадать в эту ветку"
    return client.get(url)


view_names = {
    "страница ввода логина": "meet",
    "страница игры": "game",
}


@then(parsers.parse("открывается {page_name}"))
def check_opened_page(opened_page, page_name):
    view_name = view_names.get(page_name)
    assert view_name is not None, f'"{page_name}" остсутствует в view_names'
    if opened_page.status_code == 200:
        assert opened_page.resolver_match.view_name == view_name
        assert not opened_page.has_header("location")
    elif opened_page.status_code == 302:
        assert opened_page["location"] == reverse(view_name)
    else:
        assert False, "Тест не должен попадать в эту ветку"


@when("Вася входит со своим именем", target_fixture="opened_page")
# @pytrest.mark.django_db()
def login(client, db):
    url = reverse("meet")
    return client.post(url, {"name": "Вася"})
