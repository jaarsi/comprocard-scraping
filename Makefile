setup:
	@./scripts/setup.sh
lint:
	@./scripts/lint.sh
scrape:
	@./scripts/scrape.sh
git-push:
	@./scripts/git-push.sh "$${MSG-wip}"
