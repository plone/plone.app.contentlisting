ci_tests:
	virtualenv ci_tests

ci_tests/bin/buildout: ci_tests
	ci_tests/bin/pip install -r requirements.txt

bin/test: ci_tests/bin/buildout
	ci_tests/bin/buildout -c buildout-${PLONE_VERSION}.cfg

test: bin/test
	bin/test
