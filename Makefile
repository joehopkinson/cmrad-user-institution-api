format:
	autoflake --remove-all-unused-imports --remove-unused-variables -ir src/
	autoflake --remove-all-unused-imports --remove-unused-variables -ir tests/
	isort .
	black .

run:
	docker-compose build
	docker-compose up

test:
	pytest tests/unit

simulate:
	docker-compose build
	docker-compose up -d
	python tests/simulate.py