import json

import requests as r

from .types import ScrapedPageResult, ScraperEngine


# Comprocard - https://sistemas.comprocard.com.br/GuiaCompras2021/
class ComproCardScraperEngine(ScraperEngine):
    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        response = r.post(
            "https://sistemas.comprocard.com.br/GuiaCompras2021/api/Guia/Estabelecimentos",
            headers={"Content-Type": "application/json"},
            json={"pagina": page, "qtdPorPagina": 12},
            timeout=10,
        )

        if not response.ok:
            raise Exception(response.reason)

        json_data = response.json()
        return [ComproCardScraperEngine.parse(_, page) for _ in json_data]

    @staticmethod
    def parse(item: dict, page: int) -> ScrapedPageResult:
        return {**item, "_page": page, "_source": "comprocard"}


# Alelo - https://www.alelo.com.br/onde-aceita
class AleloScraperEngine(ScraperEngine):
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
            timeout=10,
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
            "_source": "alelo",
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
            timeout=10,
        )

        if not response.ok:
            raise Exception(response.reason)

        json_data: dict = response.json()
        return [AleloScraperEngine.parse(_, page) for _ in json_data.get("establishments", [])]


# Sodexo - https://www.sodexobeneficios.com.br/sodexo-club/rede-credenciada/
class SodexoScraperEngine(ScraperEngine):
    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        return SodexoScraperEngine.fetch_page(page)

    @staticmethod
    def fetch_page(page: int) -> list[ScrapedPageResult]:
        response = r.post(
            "https://www.sodexobeneficios.com.br/sodexo/rest/accreditedNetwork/ws.accreditedNetwork.searchByProductAndAddress",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9,pt;q=0.8",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Linux"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
                "cookie": "visid_incap_2051948=nXryFf2VTKOXxn7WFaBmWaiL32UAAAAAQUIPAAAAAACFaAs+U6U4f1kwRu3zq6ja; lumClientId=2C9F81CD8DCDC31D018DF13991442F6F; nlbi_2051948=EJrkIw3WC16An8Te8iXQLgAAAAA/wYJTKxEiXQiYIlbVmuQf; incap_ses_1616_2051948=P6MCdsATslRC1EiN8i9tFnk67WUAAAAAFy8WrwSna0u3w027dV2IWg==; lumUserName=Guest; lumIsLoggedUser=false; lumUserLocale=pt_BR; JSESSIONID=73DC7AA0E19645C68C432319A3459D48.lumis2; lumUserSessionId=sbHZPZ7cSHO8oRog2W2_6OrTRIRgMqlN; AWSALB=fLFa5WE4EaJY1SaosCJVMUuilxlWz6aPbZm3I57UV/v2EHyS+6IjdMpGMSfHUjUXrgZhlJcUjbq62eirST1LFcyAXpubmEFMpnCc8i/n7ndu5B8G13ae/CDZ0X/A; AWSALBCORS=fLFa5WE4EaJY1SaosCJVMUuilxlWz6aPbZm3I57UV/v2EHyS+6IjdMpGMSfHUjUXrgZhlJcUjbq62eirST1LFcyAXpubmEFMpnCc8i/n7ndu5B8G13ae/CDZ0X/A; nlbi_2051948_2147483392=LhflBdrtJXq7SrXe8iXQLgAAAAB7tVvSdNcd7WnSAvcisu3Z; reese84=3:TYf1U6TBq1oqn8jc8iSEGA==:lJqzrhfSfStxxG4xWV/gsCzUqVpxWS+qaoWnfa+t4jLWNeU2r93uvTF4QpmGnMNoLui+4OcZepNNrmp/qxK0f2BoKmOkWJQcagi/DuPX8BkjocGqJavbzxbGs7vZQZkp8AY8I/euGNx4qK7ZyqR3pOEjLcxmNgZ0av1OMwxs1dZX+Qjdzpp7KMIdnk/Lm1YMjUV407ifeoXbXYkhnFqYvheBYG20vP/Q1qn0oRcwVFmEXdO5u9LqOUb/r1jTKyJl+cv/Cv6p3/R7df4wM7m9fcv315g/KmLjqTjw+v7/VJQ+qUaVSsFtYj5u+GLAlmGLIqenBMsirYC8ZEKSi+MMpehCjwiTSxSOHsw3eL4+2pStyEH+huyVFtKUEPAogwgBNuGSDSZ2NZCx+Lfljjz+/4uStweLbrrwk6ZunS6vgbKt0B7FuDXgI/OboIkoH5YVWZwKLx9EyOynW/AlO6tSoA==:wwCHekObMn9alq0MlsabZVL/6w2bJIPFiCqxIWfMTYE=",
                "Referer": "https://www.sodexobeneficios.com.br/",
                "Referrer-Policy": "origin",
            },
            data=f"product=526&hasDelivery=false&proximity=250km&lat=-19.61436&lon=-40.49231&startAt={(page-1)*25}",
            timeout=10,
        )

        if not response.ok:
            raise Exception(response.reason)

        json_data = json.loads(response.json()["responseData"])["hits"]["hits"]
        return [SodexoScraperEngine.parse(_["_source"], page) for _ in json_data]

    @staticmethod
    def parse(item: dict, page: int) -> ScrapedPageResult:
        return {
            "_page": page,
            "_source": "sodexo",
            "atividade": "",
            "bairro": item.get("town"),
            "cidade": item.get("city"),
            "endereco": f"{item.get('place')} {item.get('address')} {item.get('number')} {item.get('complement')}",
            "latitude": str(item.get("location")["lat"]),
            "longitude": str(item.get("location")["lon"]),
            "nome": item.get("socialname"),
            "telefone": item.get("phones"),
            "uf": item.get("state"),
        }


# Valecard - https://lojavalecard.com.br/rede/
class ValeCardScraperEngine(ScraperEngine):
    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        return []


# VR - https://www.vr.com.br/
class VRScraperEngine(ScraperEngine):
    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        return []


# UpBrasil - https://upbrasil.com/rede-credenciada
class UpBrasilScraperEngine(ScraperEngine):
    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        if page > 1:
            return []

        response = r.post(
            "https://upbrasil.com/wp-content/themes/betheme/ajax/redecredenciada.php",
            headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9,pt;q=0.8",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Linux"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
                # "cookie": "AdoptVisitorId=GwYwDARgjAnATBAtBALMYiUygDkTFAdjHwIDMzCBmHCQ4FIA; AdoptConsent=N4Ig7gpgRgzglgFwgSQCIgFwgEwHYDGAjAGYAmALAIYC0x2ArAMzXn74AM1AnJQGynUoUbPi6kopehGKUQAGhAB7AA4JkAOwAqlAOYxMAbRABHAJoBpAIIAtABK9kAOUfyQ1RQCEwAL00ANAGVUYlc4MAAnAFUAK3ZIuAFXACljAGsANygAVwBbD2w/VwBxSkcAC3Z2MCtkYph2JJhTUgBhIrLXcgBFAE8IRUVbIr9TEABdBRUEAHkshG09QzGAXyA==; SL_C_23361dd035530_SID={\"59759ca9f1252c0513700b041b9c92687554c3ba\":{\"sessionId\":\"WjQSlfd65ceMhBQOaKVoE\",\"visitorId\":\"X7XgKMD8JglNJ3m89yEoD\"}}",
                "Referer": "https://upbrasil.com/rede-credenciada",
                "Referrer-Policy": "strict-origin-when-cross-origin",
            },
            data="Latitude=-20.3196644&Longitude=-40.3384748&Radius=250&Produto=24&Cidade=Vit%C3%B3ria&Estado=ES&QRCode=0",
            timeout=60,
        )

        if not response.ok:
            raise Exception(response.reason)

        json_data = response.json().get("data", [])
        return [UpBrasilScraperEngine.parse(_, page) for _ in json_data]

    @staticmethod
    def parse(item: dict, page: int) -> ScrapedPageResult:
        *_, neigh, city, state = item.get("endereco").split(",")
        return {
            "_page": page,
            "_source": "upbrasil",
            "atividade": "",
            "bairro": neigh,
            "cidade": city,
            "endereco": item.get("endereco"),
            "latitude": str(item.get("lat")),
            "longitude": str(item.get("lng")),
            "nome": item.get("nome"),
            "telefone": item.get("telefone"),
            "uf": state,
        }


class TicketScraperEngine(ScraperEngine):
    @staticmethod
    def scrape_page_results(page: int) -> list[ScrapedPageResult]:
        response = r.post(
            "https://api.ticket.com.br/digital_redecredenciada/v2/estabelecimentos",
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9,pt;q=0.8",
                "authorization": "Bearer",
                "content-type": "application/json",
                "request-id": "1872c741-664e-449c-b566-a39b84b468f0",
                "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Linux"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "Referer": "https://www.ticket.com.br/",
                "Referrer-Policy": "origin-when-cross-origin",
            },
            json={
                "nomeEstabelecimento": None,
                "categoriaId": None,
                "raio": 300000,
                "qtdRegistro": 300,
                "longitude": -40.3384748,
                "latitude": -20.3196644,
                "produtos": ["tre"],
                "qtdPularRegistro": (page - 1) * 300,
            },
            timeout=10,
        )

        if not response.ok:
            raise Exception(response.reason)

        json_data = response.json().get("value", [])
        return [TicketScraperEngine.parse(_, page) for _ in json_data]

    @staticmethod
    def parse(item: dict, page: int) -> ScrapedPageResult:
        return {
            "_page": page,
            "_source": "ticket",
            "atividade": "",
            "bairro": item.get("bairro"),
            "cidade": item.get("cidade"),
            "endereco": item.get("endereco"),
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "nome": item.get("razaoSocial"),
            "telefone": item.get("telefone"),
            "uf": item.get("estado"),
        }
