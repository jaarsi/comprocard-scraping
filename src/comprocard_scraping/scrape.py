import os
import queue
import threading
from datetime import datetime
from time import sleep
from typing import TypedDict

import marshmallow as mm
import requests as r

from . import schemas, types


def get_page_results(page: int, results_per_page: int = 12) -> list[types.Result]:
    response = r.post(
        "https://sistemas.comprocard.com.br/GuiaCompras2021/api/Guia/Estabelecimentos",
        headers={"Content-Type": "application/json"},
        json={"pagina": page, "qtdPorPagina": results_per_page},
    )

    if not response.ok:
        raise Exception(response.reason)

    schema = schemas.ResultSchema(many=True, unknown="exclude")
    data = response.json()
    results = schema.load(data)
    return [ {**_, "_page": page } for _ in results ]


class Report(TypedDict):
    created_at: str
    errors_count: int
    objects_count: int
    objects: list[types.Result]
    errors: dict[int, str]


def get_report(concurrent_consumers: int = os.cpu_count()) -> Report:
    print(f"{concurrent_consumers=}")
    q = queue.Queue()
    report: Report = {"objects": [], "errors": {}}
    done = threading.Event()

    def consumer():
        while not done.isSet():
            try:
                page = q.get()
                print(f"\rGetting Page {page:04d}", end="")

                try:
                    if data := get_page_results(page):
                        report["objects"].extend(data)
                    else:
                        done.set()
                except mm.ValidationError as error:
                    report["errors"][page] = str(error.messages)

                q.task_done()
            except queue.Empty:
                sleep(1)

    def producer():
        page = 1
        while not done.isSet():
            try:
                q.put(page, timeout=1)
                page += 1
            except queue.Full:
                pass

    consumer_threads = [
        threading.Thread(target=consumer, daemon=True, name=f"consumer-{_}")
        for _ in range(concurrent_consumers)
    ]

    for t in consumer_threads:
        t.start()

    producer_thread = threading.Thread(target=producer, daemon=True)
    producer_thread.start()
    producer_thread.join()

    for t in consumer_threads:
        t.join()

    return {
        "created_at": datetime.now().isoformat(),
        "objects_count": len(report["objects"]),
        "errors_count": len(report["errors"]),
        **report,
    }
