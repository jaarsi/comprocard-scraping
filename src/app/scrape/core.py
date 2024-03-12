from typing import Callable

import rq
from redis import Redis

from . import engines, types

redis = Redis()
queue = rq.Queue(connection=redis)

SCRAPER_ENGINES: dict[str, types.ScraperEngine] = {
    "comprocard": engines.ComproCardScraperEngine,
    "alelo": engines.AleloScraperEngine,
    "sodexo": engines.SodexoScraperEngine,
    "upbrasil": engines.UpBrasilScraperEngine,
    "ticket": engines.TicketScraperEngine,
}


def worker(engine: types.ScraperEngine, page: int):
    if not (result := engine.scrape_page_results(page)):
        raise Exception("Empty Response")
    return result


def on_success(job, connection, result, *args, **kwargs):
    pass


def on_failure(job, connection, type, value, traceback):
    pass


def _scrape(
    engine_name: str,
    engine: types.ScraperEngine,
    on_page_handler: Callable[[str, int], None],
) -> tuple[list[types.ScrapedPageResult], dict[int, str]]:
    job = queue.enqueue(
        worker, engine, 1, on_success=rq.Callback(on_success), on_failure=rq.Callback(on_failure)
    )
    return job.latest_result(10)


def scrape(on_page_handler: Callable[[str, int], None] = None) -> list[types.ScrapedPageResult]:
    results: list[types.ScrapedPageResult] = []

    for engine_name, engine in SCRAPER_ENGINES.items():
        results.extend(_scrape(engine_name, engine, on_page_handler))

    return results
