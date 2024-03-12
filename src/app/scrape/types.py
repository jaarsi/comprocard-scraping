from typing import Protocol, TypedDict


class ScrapedPageResult(TypedDict):
    _source: str
    _page: int
    nome: str
    endereco: str
    cidade: str
    uf: str
    bairro: str
    atividade: str
    telefone: str
    latitude: float
    longitude: float


class ScraperEngine(Protocol):
    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        pass
