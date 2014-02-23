lint:
	flake8 django_twilio

test:
	python runtests.py

coverage:
	coverage run --source django_twilio run_tests.py
	coverage report -m

htmlcov:
	coverage run --source django_twilio run_tests.py
	coverage html
	open htmlcov/index.html

release:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
