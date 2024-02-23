setup:
	@scripts/setup.sh
lint:
	@scripts/lint.sh
create-report:
	@PYTHONPATH=src scripts/create-report.sh \
		--concurrency="$${concurrency-8}" \
		--results_per_page="$${results_per_page-12}"
create-report-fast:
	@PYTHONPATH=src scripts/create-report.sh --results_per_page=1000
git-push: lint
	@scripts/git-push.sh "$${MSG-wip}"
