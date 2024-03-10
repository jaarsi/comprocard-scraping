from .core import ScrapedPageResult as ScrapedPageResult
from .core import ScraperEngine
from .core import scrape as scrape
from .engines import (
    AleloScraperEngine,
    ComproCardScraperEngine,
    SodexoScraperEngine,
    UpBrasilScraperEngine,
    ValeCardScraperEngine,
    VRScraperEngine,
)

SCRAPER_ENGINES: dict[str, ScraperEngine] = {
    "comprocard": ComproCardScraperEngine,
    "alelo": AleloScraperEngine,
    "sodexo": SodexoScraperEngine,
    "vr": VRScraperEngine,
    "valecard": ValeCardScraperEngine,
    "upbrasil": UpBrasilScraperEngine,
}
