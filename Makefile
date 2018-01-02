VIRTUALENV = $(shell which virtualenv)

ifeq ($(strip $(VIRTUALENV)),)
  VIRTUALENV = /usr/local/python/bin/virtualenv
endif

venv:
	$(VIRTUALENV) venv

venv3:
	python3 -m venv venv3

install: venv
	. venv/bin/activate; pip install -r requirements.txt

install3: venv3
	 . venv3/bin/activate; pip install -r requirements.txt

install-test: venv install
	. venv/bin/activate; pip install -r test_requirements.txt

install-test3: venv3 install
	 . venv3/bin/activate; pip install -r test_requirements.txt

lint: venv
	. venv/bin/activate; flake8 django_twilio/ --exclude=*migrations
lint3: venv3
	. venv3/bin/activate; flake8 django_twilio/ --exclude=*migrations

test: venv
	. venv/bin/activate; python manage.py test

test3: venv3
	. venv3/bin/activate; python manage.py test


coverage: venv
	. venv/bin/activate; coverage run --source django_twilio manage.py test

coverage3: venv3
	. venv3/bin/activate; coverage run --source django_twilio manage.py test

htmlcov: venv
	. venv/bin/activate; coverage run --source django_twilio manage.py test
	coverage html
	open htmlcov/index.html
htmlcov3: venv3
	. venv3/bin/activate; coverage run --source django_twilio manage.py test
	coverage html
	open htmlcov/index.html

release: venv
	. venv/bin/activate; python setup.py sdist upload
	. venv/bin/activate; python setup.py bdist_wheel upload

release3: venv3
	. venv3/bin/activate; python setup.py sdist upload
	. venv3/bin/activate; python setup.py bdist_wheel upload


build: venv
	. venv/bin/activate; python setup.py sdist
	. venv/bin/activate; python setup.py bdist_wheel

build3: venv3
	. venv3/bin/activate; python setup.py sdist
	. venv3/bin/activate; python setup.py bdist_wheel


shell: venv
	. venv/bin/activate; python manage.py shell

shell3: venv3
	. venv3/bin/activate; python manage.py shell


clean:
	rm -rf docs/build
	rm -rf django_twilio.egg-info
	rm -rf htmlcov
	rm -rf dist
	rm -rf build/
