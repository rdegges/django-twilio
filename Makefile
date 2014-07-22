lint:
	flake8 django_twilio --exclude=migrations

test:
	python manage.py test

coverage:
	coverage run --source django_twilio manage.py test
	coverage report -m

htmlcov:
	coverage run --source django_twilio manage.py test
	coverage html
	open htmlcov/index.html

release:
	python setup.py sdist upload
	python setup.py bdist_wheel upload

build:
	python setup.py sdist
	python setup.py bdist_wheel
