setup:
	@./scripts/setup.sh
lint:
	@poetry run pre-commit run -a
scrape:
	@./scripts/scrape.sh
git-push:
	@git add .
	@git commit -m "wip"