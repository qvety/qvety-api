.PHONY: runserver
runserver:
	python3 manage.py runserver

.PHONY: makemigrations
makemigrations:
	python3 manage.py makemigrations

.PHONY: migrate
migrate:
	python3 manage.py migrate

.PHONY: createsuperuser
createsuperuser:
	python3 manage.py createsuperuser

.PHONY: docker-up
docker-up:
	docker-compose -f docker-compose.dev.yaml up -d

.PHONY: docker-down
docker-down:
	docker-compose -f docker-compose.dev.yaml down

.PHONY: lint
lint:
	sh run_linters.sh

.PHONY: tests
tests:
	python3 manage.py test