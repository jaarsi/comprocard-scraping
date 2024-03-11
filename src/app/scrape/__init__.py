from .core import ScrapedPageResult as ScrapedPageResult
from .core import ScraperEngine
from .core import scrape as scrape
from .engines import (  # ValeCardScraperEngine,; VRScraperEngine,
    AleloScraperEngine,
    ComproCardScraperEngine,
    SodexoScraperEngine,
    TicketScraperEngine,
    UpBrasilScraperEngine,
)

SCRAPER_ENGINES: dict[str, ScraperEngine] = {
    "comprocard": ComproCardScraperEngine,
    "alelo": AleloScraperEngine,
    "sodexo": SodexoScraperEngine,
    "upbrasil": UpBrasilScraperEngine,
    "ticket": TicketScraperEngine,
}
