# Copyright (c) 2019 YugaByte, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.  See the License for the specific language governing permissions and limitations under
# the License.

SHELL:=bash

.PHONY: docs list release setup test tox unit venv venv_tests venv_docs venv_release

ACTIVATE_VENV := . venv/bin/activate
RUN_TESTS := nosetests tests

test: venv_tests
	$(ACTIVATE_VENV) && $(RUN_TESTS)

test_no_venv: venv_tests
	$(RUN_TESTS)

# install all dependencies
setup: venv_tests venv_docs venv_release

# run tests against all supported python versions
tox: venv_tests
	$(ACTIVATE_VENV) && tox

release: tox venv_release
	rm -f dist/*
	#. venv/bin/activate && python relocate/update_version.py
	$(ACTIVATE_VENV) && python setup.py sdist
	#. venv/bin/activate && twine upload dist/relocate*.tar.gz

docs: venv_docs
	$(ACTIVATE_VENV) && cd docs && make html

venv: venv_tests venv_docs venv_release

venv_create:
	if [[ ! -d venv ]]; then \
		python3 -m virtualenv venv; \
	fi

venv_tests: venv_create
	$(ACTIVATE_VENV) && pip install --editable ".[tests]"

venv_docs: venv_create
	$(ACTIVATE_VENV) && pip install --editable ".[docs]"

venv_release: venv_release
	$(ACTIVATE_VENV) && pip install --editable ".[release]"
