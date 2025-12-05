.PHONY: m1
m1:
	src/manage.py makemigrations
.PHONY: m2
m2:
	src/manage.py migrate
.PHONY: mm
mm:
	src/manage.py makemigrations && src/manage.py migrate
