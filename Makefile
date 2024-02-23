setup:
	@scripts/setup.sh
lint:
	@poetry run scripts/lint.sh
create-report:
	@poetry run scripts/create-report.sh \
		--concurrency="$${concurrency-8}" \
		--results_per_page="$${results_per_page-12}"
create-report-fast:
	@poetry run scripts/create-report.sh --results_per_page=1000
git-push: lint
	@poetry run scripts/git-push.sh "$${MSG-wip}"
clear-reports:
	@rm -rf reports/*.csv reports/*.json
docker-build:
	@docker build -t comprocard-scraping:latest .
docker-run: docker-build
	@docker run -it --rm -v "./reports:/app/reports" comprocard-scraping:latest \
		--concurrency="$${concurrency-8}" \
		--results_per_page="$${results_per_page-12}"
create-requirements-file:
	@poetry export > requirements.txt
