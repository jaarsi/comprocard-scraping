from . import engines
from .core import ScrapedPageResult as ScrapedPageResult
from .core import ScraperEngine
from .core import scrape as scrape

SCRAPER_ENGINES: list[ScraperEngine] = [
    engines.ComproCardScraperEngine,
    engines.AleloScraperEngine,
    engines.SodexoScraperEngine,
    engines.VRScraperEngine,
    engines.ValeCardScraperEngine,
    engines.UpBrasilScraperEngine,
]
