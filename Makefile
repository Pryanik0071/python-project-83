PORT ?= 8000

install:
	poetry install

package-install:
	python3 -m pip install dist/*.whl --force-reinstall

lint:
	poetry run flake8 page_analyzer

dev:
	poetry run flask --app page_analyzer:app --debug run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh
