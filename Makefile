.PHONY: help
help:
	# HELP
	#   make m1 - makemigrations
	#   make m2 - migrate
	#   make mm - makemigrations and migrate
	#   make del_db - delete db
	#   make cmm - delete db, makemigrations and migrate
	#   make check - run linters
	#   make test - run pytest

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

.PHONY: del_db
del_db:
	rm -f src/db.sqlite3||echo File not found

.PHONY: cmm
cmm: del_db mm

.PHONY: check
check:
	uv run ruff check --fix
	uv run ruff format

.PHONY: test
test:
	pytest -vv --lf --cov --cov-report html --cov-append
