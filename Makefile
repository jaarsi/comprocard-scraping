setup:
	@poetry lock
	@poetry install --no-root --with dev
lint:
	@poetry run scripts/lint.sh
create-report:
	@poetry run scripts/create-report.sh "$${ARGS}"
git-push: create-requirements-file lint
	@git add .
	@git commit -m wip
	@git push
clear-reports:
	@rm -rf reports/*.csv reports/*.json
docker-build: create-requirements-file
	@docker build -t zd-scraping:latest .
docker-run: docker-build
	@docker run -it --rm -v "./reports:/app/reports" zd-scraping:latest "$${ARGS}"
create-requirements-file:
	@poetry export -q -o requirements.txt
