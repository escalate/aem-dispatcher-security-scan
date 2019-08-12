.PHONY: venv
venv: clean
	python3 -m venv venv

.PHONY: requirements
requirements:
	pip install --upgrade --requirement requirements.txt

.PHONY: dev-requirements
dev-requirements: requirements
	pip install --upgrade --requirement dev-requirements.txt

.PHONY: test
test:
	tox

.PHONY: clean
clean:
	rm -rf venv/
	py3clean .

.PHONY: build
build:
	docker build \
		--tag=scan \
		.
