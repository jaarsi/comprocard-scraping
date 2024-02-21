from typing import TypedDict


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
