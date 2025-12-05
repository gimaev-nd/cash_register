.PHONY: m1
m1:
	src/manage.py makemigrations
	uv run ruff check --fix
.PHONY: m2
m2:
	src/manage.py migrate
.PHONY: mm
mm:
	src/manage.py makemigrations
	src/manage.py migrate
	uv run ruff check --fix
