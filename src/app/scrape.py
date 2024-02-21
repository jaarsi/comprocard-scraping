import os
import queue
import threading
from typing import TypedDict

import marshmallow as mm
import requests as r


class Result(TypedDict):
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


class PageItemSchema(mm.Schema):
    nome = mm.fields.String(load_default=None)
    endereco = mm.fields.String(load_default=None)
    cidade = mm.fields.String(load_default=None)
    uf = mm.fields.String(load_default=None)
    bairro = mm.fields.String(load_default=None)
    atividade = mm.fields.String(load_default=None)
    telefone = mm.fields.String(load_default=None)
    latitude = mm.fields.String(load_default=None)
    longitude = mm.fields.String(load_default=None)



def get_page_results(page: int, results_per_page: int = 12) -> list[Result]:
    response = r.post(
        "https://sistemas.comprocard.com.br/GuiaCompras2021/api/Guia/Estabelecimentos",
        headers={"Content-Type": "application/json"},
        json={"pagina": page, "qtdPorPagina": results_per_page},
    )

    if not response.ok:
        raise Exception(response.reason)

    schema = PageItemSchema(many=True, unknown="exclude")
    data = response.json()
    results = schema.load(data)
    return [{**_, "_page": page} for _ in results]


def get_all_results(concurrency: int = os.cpu_count()) -> list[Result]:
    print(f"{concurrency=}")
    q = queue.Queue()
    done = threading.Event()
    results = []

    def consumer():
        while not done.isSet():
            try:
                page = q.get()
                print(f"\rRetrieving data from page {page:04d}", end="")

                if data := get_page_results(page):
                    results.extend(data)
                else:
                    done.set()

                q.task_done()
            except queue.Empty:
                pass

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
        for _ in range(concurrency)
    ]

    for t in consumer_threads:
        t.start()

    producer_thread = threading.Thread(target=producer, daemon=True)
    producer_thread.start()
    producer_thread.join()

    for t in consumer_threads:
        t.join()

    return results
