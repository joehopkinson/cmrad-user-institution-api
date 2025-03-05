format:
	autoflake --remove-all-unused-imports --remove-unused-variables -ir src/
	autoflake --remove-all-unused-imports --remove-unused-variables -ir tests/
	isort .
	black .

make lint:
	mypy src/

run:
	docker-compose build
	docker-compose up