import requests as r

from .core import ScrapedPageResult, ScrapedPageResultSchema, ScraperEngine


# Comprocard - https://sistemas.comprocard.com.br/GuiaCompras2021/
class ComproCardScraperEngine(ScraperEngine):
    name = "comprocard"

    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        response = r.post(
            "https://sistemas.comprocard.com.br/GuiaCompras2021/api/Guia/Estabelecimentos",
            headers={"Content-Type": "application/json"},
            json={"pagina": page, "qtdPorPagina": 12},
            timeout=5,
        )

        if not response.ok:
            raise Exception(response.reason)

        data = response.json()
        schema = ScrapedPageResultSchema(many=True, unknown="exclude")
        results = schema.load(data)
        return [{**_, "_page": page, "_source": ComproCardScraperEngine.name} for _ in results]


# Alelo - https://www.alelo.com.br/onde-aceita
class AleloScraperEngine(ScraperEngine):
    name = "alelo"
    reference_points = [
        (-21.17172, -41.38435),
        (-20.40012, -40.93867),
        (-19.59873, -40.48750),
        (-18.73080, -40.35544),
        (-18.27164, -40.37195),
    ]

    @staticmethod
    def get_token() -> str:
        response = r.post(
            "https://api.alelo.com.br/alelo/prd/cardholders/oauth2/token",
            headers={
                "accept": "application/json, text/plain, */*, application/json",
                "accept-language": "en-US,en;q=0.9,pt;q=0.8",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Linux"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "Referer": "https://redeaceitacao.alelo.com.br/",
                "Referrer-Policy": "strict-origin-when-cross-origin",
            },
            data="grant_type=client_credentials&client_id=76a775cd-8b2c-4ce8-b7a5-b321c66223f7&client_secret=V2jC1qG2dN2nQ2sK3gE7hR0tI1oO3yT4oF0tA3iI5qK8gD7fX7&scope=acceptance-network",
        )

        if not response.ok:
            raise Exception(response.reason)

        return response.json()["access_token"]

    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        return AleloScraperEngine.fetch_page(page)

    @staticmethod
    def parse(item: dict, page: int) -> ScrapedPageResult:
        return {
            "_source": AleloScraperEngine.name,
            "_page": page,
            "atividade": "",
            "bairro": item.get("district"),
            "cidade": item.get("cityName"),
            "endereco": f"{item.get('address')}, {item.get('addressNumber')}, {item.get('complement')}",
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "nome": item.get("establishmentSocialReason"),
            "telefone": f"{item.get('phoneAreaCode')} {item.get('phoneNumber')}",
            "uf": item.get("stateName"),
        }

    @staticmethod
    def fetch_page(page: int, results_per_page: int = 300) -> list[ScrapedPageResult]:
        token = AleloScraperEngine.get_token()
        return [
            _
            for lat, long in AleloScraperEngine.reference_points
            for _ in AleloScraperEngine._fetch_page(page, results_per_page, lat, long, token)
        ]

    @staticmethod
    def _fetch_page(
        page: int, results_per_page: int, lat: int, long: int, token: str, distance: int = 100
    ) -> list[ScrapedPageResult]:
        url = (
            "https://api.alelo.com.br/alelo/prd/acceptance-network/establishments?"
            f"longitude={long}&latitude={lat}&distance={distance}&pageNumber={page}"
            f"&pageSize={results_per_page}&type=POSITION"
        )
        response = r.get(
            url,
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9,pt;q=0.8",
                "authorization": f"Bearer {token}",
                "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Linux"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "x-ibm-client-id": "76a775cd-8b2c-4ce8-b7a5-b321c66223f7",
                "Referer": "https://redeaceitacao.alelo.com.br/",
                "Referrer-Policy": "strict-origin-when-cross-origin",
            },
        )

        if not response.ok:
            raise Exception(response.reason)

        json_data: dict = response.json()
        return [AleloScraperEngine.parse(_, page) for _ in json_data.get("establishments", [])]


# Sodexo - https://www.sodexobeneficios.com.br/sodexo-club/rede-credenciada/
class SodexoScraperEngine(ScraperEngine):
    name = "sodexo"

    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        return []


# Valecard - https://lojavalecard.com.br/rede/
class ValeCardScraperEngine(ScraperEngine):
    name = "valecard"

    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        return []


# VR - https://www.vr.com.br/
class VRScraperEngine(ScraperEngine):
    name = "vr"

    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        return []


# UpBrasil - https://upbrasil.com/rede-credenciada
class UpBrasilScraperEngine(ScraperEngine):
    name = "upbrasil"

    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        return []
