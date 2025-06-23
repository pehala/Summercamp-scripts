.PHONY: commit-acceptance black pylint munchkin vampires program

SECRET_FILE ?= client_secret.json

black: ## Checks black
	poetry run black --check . --diff

commit-acceptance: black

munchkin: ## Generates Munchkin-like cards
	@test -n "$(SPREADSHEET)"
	poetry run python -m munchkin -s $(SECRET_FILE) $(SPREADSHEET)

vampires: ## Generates Vampire riddles cards
	@test -n "$(SPREADSHEET)"
	poetry run python -m vampires -s $(SECRET_FILE) $(SPREADSHEET)

program: ## Generates program summary of the entire camp
	@test -n "$(SPREADSHEET)"
	@test -n "$(DATE)"
	poetry run python -m program -d $(DATE) -s $(SECRET_FILE) $(SPREADSHEET)

clean: ## Cleans output
	rm -rf output/


# Check http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Print this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)