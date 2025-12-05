from users.models import Gamer


def create_gamer(name: str) -> Gamer:
    return Gamer.objects.get_or_create(name=name)[0]
