setup:
	@scripts/setup.sh
lint:
	@scripts/lint.sh
create-report:
	@PYTHONPATH=src scripts/create-report.sh
git-push: lint
	@scripts/git-push.sh "$${MSG-wip}"
