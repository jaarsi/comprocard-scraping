install-dev:
	@scripts/install-dev.sh
install:
	@scripts/install.sh
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
clear-reports:
	@rm -rf reports/*.csv reports/*.json
docker-build:
	@docker build -t comprocard-scraping:latest .
docker-run:
	@docker run -it --rm -v "./reports:/app/reports" comprocard-scraping:latest \
		results_per_page=1000
