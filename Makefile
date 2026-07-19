.PHONY: install lint format test run docker-build docker-run

install:
	pip install -r requirements.txt -r requirements-dev.txt

lint:
	flake8 app tests --max-line-length=100

format:
	black app tests

test:
	pytest --cov=app --cov-report=term-missing

run:
	python -m app.main

docker-build:
	docker build -t task-api:local .

docker-run:
	docker run --rm -p 5000:5000 task-api:local
