py := pdm run
package_dir := src
tests_dir := tests
code_dir := $(package_dir)

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Lint source code
	$(py) mypy $(code_dir) || true

.PHONY: install
install: ## Install all depends
	pdm install -G:all

.PHONY: update
update: ## Update all depends
	pdm update --update-all