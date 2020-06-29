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