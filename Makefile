.PHONY: setup-env
setup-env:
	python3 -m venv venv
	bash -c "source venv/bin/activate"
	pip3 install -r requirements.txt
	pip3 install -e .

.PHONY: clean
clean:
	rm -rf .tox
	rm -rf nosetests.xml

.PHONY: test
test:
	tox -e pytest

.PHONY: lint
lint:
	tox -e pylint