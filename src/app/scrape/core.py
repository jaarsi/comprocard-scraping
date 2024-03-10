import queue
import threading
from typing import Callable, Protocol, TypedDict

import marshmallow as mm


class ScrapedPageResult(TypedDict):
    nome: str
    endereco: str
    cidade: str
    uf: str
    bairro: str
    atividade: str
    telefone: str
    latitude: float
    longitude: float
    _page: int
    _source: str


class ScrapedPageResultSchema(mm.Schema):
    nome = mm.fields.String(load_default=None)
    endereco = mm.fields.String(load_default=None)
    cidade = mm.fields.String(load_default=None)
    uf = mm.fields.String(load_default=None)
    bairro = mm.fields.String(load_default=None)
    atividade = mm.fields.String(load_default=None)
    telefone = mm.fields.String(load_default=None)
    latitude = mm.fields.String(load_default=None)
    longitude = mm.fields.String(load_default=None)


class ScraperEngine(Protocol):
    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        pass


def scrape(
    engine: ScraperEngine,
    concurrency: int,
    progress_handler: Callable[[int], None],
) -> tuple[list[ScrapedPageResult], dict[int, str]]:
    q = queue.Queue(concurrency)
    done = threading.Event()
    results = []
    errors = {}

    def consumer():
        while not done.is_set():
            try:
                page = q.get(timeout=1)
                progress_handler(page)

                if not (data := engine.scrape_page_results(page)):
                    done.set()
                    break

                results.extend(data)
            except queue.Empty:
                pass
            except Exception as error:
                errors[page] = repr(error)
            finally:
                q.task_done()

    def producer():
        page = 1
        while not done.is_set():
            q.put(page)
            page += 1

    producer_thread = threading.Thread(target=producer, daemon=True, name="producer-0")
    producer_thread.start()
    consumer_threads = [
        threading.Thread(target=consumer, daemon=True, name=f"consumer-{_}")
        for _ in range(concurrency)
    ]

    for t in consumer_threads:
        t.start()

    for t in consumer_threads:
        t.join()

    return results, errors