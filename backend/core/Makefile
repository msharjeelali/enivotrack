run:
	python manage.py runserver 0.0.0.0:8002

migrate:
	python manage.py makemigrations
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic --noinput

test:
	python manage.py test

flush:
	python manage.py flush

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

check:
	ruff check .

fix:
	ruff check --fix .
	ruff format .