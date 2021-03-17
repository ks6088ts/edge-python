PYFILES := $(shell find . -type d -name .venv -prune -o -type f -name '*.py' -print)
POETRY_RUN := poetry run
VENV_CREATE := true # set false for global install
VENV_IN_PROJECT := true

# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

.PHONY: clean
clean: ## clean
	rm -rf .venv

.PHONY: install
install: ## install
	python -m pip install --upgrade pip
	pip install poetry
	poetry config virtualenvs.create $(VENV_CREATE)
	poetry config virtualenvs.in-project $(VENV_IN_PROJECT)
	poetry install

.PHONY: format
format: ## format codes
	$(POETRY_RUN) isort $(PYFILES)
	$(POETRY_RUN) black $(PYFILES)

.PHONY: lint
lint: ## lint codes
	$(POETRY_RUN) pylint $(PYFILES)

.PHONY: test
test: ## test codes
	$(POETRY_RUN) pytest --capture=no $(PYFILES)

.PHONY: ci
ci: format lint test ## run ci tests
