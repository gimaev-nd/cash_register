.PHONY: help
help:
	echo m1, m2, mm, cmm, check, test

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

.PHONY: test
test:
	pytest --lf --cov --cov-report html
