py := pdm run

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Run tests
	$(py) pytest -v

.PHONY: lint
lint: ## Lint source code
	$(py) pre-commit run --all-files

.PHONY: install
install: ## Install all depends
	pdm install -G:all
	$(py) pre-commit install

.PHONY: update
update: ## Update all depends
	pdm update --update-all
	$(py) pre-commit autoupdate
