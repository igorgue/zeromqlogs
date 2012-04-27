all: test_pretty

PACKAGE_NAME = zmqlogs

TESTS_DEPENDENCIES = nose pinocchio mock

# Nose stuff to run single, type or all.
NOSE_SINGLE_FLAGS = -sd
NOSE_SHORT_FLAGS = ${NOSE_SINGLE_FLAGS} --verbosity=2
NOSE_LONG_FLAGS = ${NOSE_SHORT_FLAGS} --with-coverage --cover-erase --cover-inclusive --cover-package=${PACKAGE_NAME}
NOSE_LONG_COLOR_FLAGS = ${NOSE_LONG_FLAGS} --with-spec --spec-color

init: check_deps
	@pip install -r requirements.txt --use-mirrors

test: check_deps
	@nosetests ${NOSE_LONG_FLAGS} --quickunit-prefix=tests/unit/ --quickunit-prefix=tests/integration/ --quickunit-prefix=tests/functional/

test_pretty: check_deps
	@nosetests ${NOSE_LONG_COLOR_FLAGS} --quickunit-prefix=tests/unit/ --quickunit-prefix=tests/integration/ --quickunit-prefix=tests/functional/

unit: check_deps
	@nosetests ${NOSE_SHORT_FLAGS} --quickunit-prefix=tests/unit/

integration: check_deps
	@nosetests ${NOSE_SHORT_FLAGS} --quickunit-prefix=tests/integration/

functional: check_deps
	@nosetests ${NOSE_SHORT_FLAGS} --quickunit-prefix=tests/functional/

run_test: check_deps
ifndef TEST
	@echo "Please pass TEST=test_file.py as argument to run_test (e.g.: make run-test TEST=tests/unit/test_serialization.py)"
else
	@nosetests ${NOSE_SINGLE_FLAGS} ${TEST}
endif

check_deps:
	@for dependency in ${TESTS_DEPENDENCIES}; do \
		python -c "import $$dependency" 2>/dev/null || (echo "Install $$dependency to run zmqlogs's tests. Try: make init" && exit 3) ; \
		done

