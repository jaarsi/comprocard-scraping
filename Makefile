setup:
	@scripts/setup.sh
lint:
	@scripts/lint.sh
create-report:
	@PYTHONPATH=src scripts/create-report.sh \
		--concurrency="$${concurrency-8}" \
		--results_per_page="$${results_per_page-12}"
git-push: lint
	@scripts/git-push.sh "$${MSG-wip}"
